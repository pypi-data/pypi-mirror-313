#import inotify.adapters
import threading
import os
import time
from . import worker
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import fnmatch
import re

def print_new_file(filename):
    print(f"new file created: {filename}")

class CustomEventHandler(FileSystemEventHandler):
    def __init__(self, callbacks=[print_new_file], pattern='*'):
        super().__init__()
        self.callbacks = callbacks
        self.pending = set()
        self.filt = re.compile(fnmatch.translate(pattern))

    def on_created(self, event):
        # we want to trigger only when the creation of a new file complete
        # so the creation is buffered and checked at closing time
        if self.filt.match(event.src_path):
            self.pending.add(event.src_path)

    def on_closed(self, event):
        if event.src_path in self.pending:
            self.pending.remove(event.src_path)
            for c in self.callbacks:
                c(event.src_path)

    def on_moved(self, event):
        if self.filt.match(event.dest_path):
            for c in self.callbacks:
                c(event.dest_path)
    
class NewFileWatcher(worker.Worker):
    '''A specific class of worker whose role is to push tasks to
    segments every time a new file is available in a directory

    '''
    def __init__(self, addr, env, directories, process_name, pattern='*'):
        worker.Worker.__init__(self, addr, env)
        self.notification_setup(directories, process_name, pattern)
    
    def notification_setup(self, directories, process_name, pattern):
        self.process_name = process_name
        self.observer = Observer()
        for directory in directories:
            # Schedule the event handler with the observer for each directory
            self.observer.schedule(CustomEventHandler([self.push_task], pattern),
                                   directory, recursive=True)
    
    def process(self):
        # With watchdog, we don't need to manually loop through events here 
        # as they are handled by the event handler. However, we might want 
        # to keep the worker alive or do other tasks.
        self.observer.start()  # Start the observer thread
        try:
            while self.running and threading.main_thread().is_alive():
                time.sleep(1)  # Keep the main thread alive or do other work
        finally:
            self.observer.stop()
            self.observer.join()
        print(f'NewFileWatcher {self.wid} complete.')
    
    def push_task(self, filename):
        with self.comm_lock:
            try:
                self.server.push_task(self.process_name, filename)
            except Exception as e:
                print(f'Caught an unexpected exception: {type(e).__name__} - {e}, going down')
                self.running = False


class PollingWorker(worker.Worker):
    ''' A simple worker doing a simple task until killed
    '''
    def __init__(self, addr, env, process, interval=2):
        worker.Worker.__init__(self, addr, env)
        self._process = process
        self.interval = interval
        
    def process(self):
        last=0
        while self.running and threading.main_thread().is_alive():
            if time.time()-last > self.interval:
                last=time.time()
                try:
                    self._process()
                except Exception as e:
                    print(e)
            time.sleep(0.1)

        print(f'PollingWorker {self.wid} complete.')
