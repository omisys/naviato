import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from client import Client


class Watcher:

    def __init__(self, watchdir):
        self.observer = Observer()
        self.watchdir = watchdir

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


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):

        if event.event_type == 'created':
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'deleted':
            print("Received deleted event - %s." % event.src_path)

        elif event.event_type == 'modified':
            Client.print_change(bitch)
            print("Received modified event - %s." % event.src_path)

        elif event.event_type == 'moved':
            print("Received moved event - from %s to %s." % (event.src_path, event.dest_path))


if __name__ == '__main__':
    w = Watcher()
    w.run()
