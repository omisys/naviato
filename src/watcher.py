import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot,DirectorySnapshotDiff

class Watcher:

    def __init__(self, watchdir):
        self.observer = Observer()
        self.watchdir = watchdir
        self._started = False

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchdir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()

    def scan(self):
        if not self._started:
            self._started = True
            self._newSnap = DirectorySnapshot(path=self.watchdir, recursive=True)
            self._oldSnap = self._newSnap
            print(self._newSnap)
            return None
        else:
            self._newSnap  = DirectorySnapshot(path=self.watchdir, recursive=True)
            self._diffSnap = DirectorySnapshotDiff(self._oldSnap, self._newSnap)
            self._oldSnap  = self._newSnap
            return self._diffSnap
            #self.process_diff()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):

        if not event.is_directory:
            # switch event type
            if event.event_type == 'created':
                print("new file: {}".format(event.src_path))

            elif event.event_type == 'deleted':
                print("del file: {}".format(event.src_path))

    @staticmethod
    def on_modified(event):
        print("mod file: {}".format(event.src_path))
