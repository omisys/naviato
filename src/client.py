#!/usr/bin/env python3

### client.py ###
import os
import time
import getpass
import configparser
from filetransfer import Filetransfer
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

WATCH_TIME = 5

class Client:

    def __init__(self, conf_path):
        # get the absolute path to the current directory
        self.abs_file_path = os.path.abspath(os.path.dirname(__file__))
        self.config_path = os.path.join(self.abs_file_path, conf_path)

    def read_config(self):
        config = configparser.RawConfigParser()
        config.read(self.config_path)
        self._host = config.get('example-config', 'host')
        self._port = int(config.get('example-config', 'port'))

    def get_home_dir():
        return os.path.join("/home", getpass.getuser())

    def watch(self, watchdir=None, recursive=True):
        if not watchdir:
            watchdir = input("Enter directory to monitor: ")
        self.watchdir = watchdir
        self.recursive = recursive
        self._started = False

    def scan(self):
        if not self._started:
            self._started = True
            self._newSnap = DirectorySnapshot(path=self.watchdir, recursive=self.recursive)
            self._oldSnap = self._newSnap
            #print(self._newSnap)
        else:
            self._newSnap  = DirectorySnapshot(path=self.watchdir, recursive=self.recursive)
            self._diffSnap = DirectorySnapshotDiff(self._oldSnap, self._newSnap)
            self._oldSnap  = self._newSnap
            self.process_diff()
        return

    def process_diff(self):
        # Put all process functions for files and dirs here
        self.process_files_created()
        self.process_files_modified()

    def process_files_created(self):
        for f in self._diffSnap.files_created:
            filepath = f
            filename = f.split("/")[-1]
            print("New file created: {}".format(filename))

            try:
                send = Filetransfer()

                send.send_init(self._host, self._port)
                send.send_filename(filename)
                send.send_filesize(filepath)
                send.send_chunk()
                send.close_socket()
            except:
                print("Failed to transfer: {}".format(filename))

    def process_files_modified(self):
        for f in self._diffSnap.files_modified:
            filepath = f
            filename = f.split("/")[-1]
            print("File modified: {}".format(filename))


def main():
    # Make new client and read config
    c = Client("../config")
    c.read_config()

    # Set the directory to watch
    c.watch(recursive=False)

    # main loop
    while True:
        c.scan()
        time.sleep(WATCH_TIME)


if __name__ == "__main__":
    main()
