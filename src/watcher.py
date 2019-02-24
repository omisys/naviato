#!/usr/bin/env python3

### watcher.py ###
import time
from filetransfer import Filetransfer
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

class Watcher:

    def __init__(self, watchdir=None, recursive=True):
        if not watchdir:
            watchdir = input("Enter directory to monitor: ")

        self.watchdir  = watchdir
        self.recursive = recursive
        self._started  = False

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
        self.process_files_moved()
        self.process_files_deleted()
        self.process_dirs_created()
        self.process_dirs_modified()
        self.process_dirs_moved()
        self.process_dirs_deleted()

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

    def process_files_moved(self):
        for f in self._diffSnap.files_moved:
            filepath = f
            filename = f.split("/")[-1]
            print("File moved: {}".format(filename))

    def process_files_deleted(self):
        for f in self._diffSnap.files_deleted:
            filepath = f
            filename = f.split("/")[-1]
            print("File deleted: {}".format(filename))

    def process_dirs_created(self):
        for d in self._diffSnap.dirs_created:
            dirpath = d
            print (dirpath)
            dirname = d.split("/")[-1]
            print("New dir created: {}".format(dirname))

    def process_dirs_modified(self):
        for d in self._diffSnap.dirs_modified:
            dirpath = d
            dirname = d.split("/")[-1]
            print("Dir modified: {}".format(dirname))

    def process_dirs_moved(self):
        for (old_path, new_path) in self._diffSnap.dirs_moved:
            oldpath = old_path
            oldname = old_path.split("/")[-1]
            newpath = new_path
            newname = new_path.split("/")[-1]
            print("Dir moved: {} to {}".format(old_path, new_path))

    def process_dirs_deleted(self):
        for d in self._diffSnap.dirs_deleted:
            dirpath = d
            dirname = d.split("/")[-1]
            print("Dir deleted: {}".format(dirname))
