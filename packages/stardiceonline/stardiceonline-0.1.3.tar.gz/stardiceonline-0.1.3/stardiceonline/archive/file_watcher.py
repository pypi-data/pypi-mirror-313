import inotify.adapters
import threading
import os

def print_event(event):
    (_, type_names, path, filename) = event
    print(f"PATH=[{path}] FILENAME=[{filename}] EVENT_TYPES={type_names}")

def print_new_file(filename):
    print(f"new file created: {filename}")

class Watcher(object):
    def __init__(self, directory, actions=[print_event]):
        self.directory = directory
        self.notif = inotify.adapters.Inotify()
        self.notif.add_watch(self.directory)
        self.actions = actions
        self.active = True
        self._stop = False
        self.thread = None
        
    def __call__(self):
        while (not self._stop) and threading.main_thread().is_alive():
            for event in self.notif.event_gen(yield_nones=False, timeout_s=.2):
                if self.active:
                    for a in self.actions:
                        a(event)
                if self._stop:
                    break

            
    def watch(self):
        self._stop = False
        self.thread = threading.Thread(target=self)
        self.thread.start()

    def stop(self):
        self._stop = True
        if self.thread:
            self.thread.join()
        
    def __del__(self):
        self.stop()


class NewFileReady(object):
    def __init__(self, directory, callbacks=[print_new_file], debug=False):
        if debug:
            self.watcher = Watcher(directory, [self, print_event])
        else:
            self.watcher = Watcher(directory, [self])
        self.pending_new_files = []
        self.lock = threading.Lock()
        self.callbacks = callbacks
        
    def __call__(self, event):
        (_, type_names, path, filename) = event
        if ('IN_CREATE' in type_names):
            with self.lock:
                self.pending_new_files.append(os.path.join(path, filename))
        if ('IN_CLOSE_WRITE' in type_names):
            fname = os.path.join(path, filename)
            if fname in self.pending_new_files:
                with self.lock:
                    self.pending_new_files.remove(fname)
                for callback in self.callbacks:
                    callback(fname)
        if ('IN_MOVED_TO' in type_names):
            fname = os.path.join(path, filename)
            for callback in self.callbacks:
                callback(fname)
                    
    def watch(self):
        self.watcher.watch()

    def stop(self):
        self.watcher.stop()
        
if __name__ == '__main__':
    w = NewFileReady('/tmp')
    w.watch()
