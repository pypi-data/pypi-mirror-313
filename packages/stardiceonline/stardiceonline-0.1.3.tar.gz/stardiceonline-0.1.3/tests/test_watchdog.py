from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent, FileMovedEvent
import threading
import time
import fnmatch
import re


class CustomEventHandler(FileSystemEventHandler):
    def __init__(self, pattern='*'):
        super().__init__()
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
            print(f'new file {event.src_path}')

    def on_moved(self, event):
        if self.filt.match(event.dest_path):
            print(f'new file {event.dest_path}')
        
observer = Observer()
observer.start()  # Start the observer thread

observer.schedule(CustomEventHandler('*.fits'), '/home/betoule/ohp_archive/2024_10_10/', recursive=True)
try:
    while threading.main_thread().is_alive():
        time.sleep(1)  # Keep the main thread alive or do other work
except KeyboardInterrupt:
    observer.stop()
observer.join()
print(f'NewFileWatcher complete.')
    
