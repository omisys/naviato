#!/usr/bin/env python3

### watcher.py ###
import time
import os.path
import json
from pathlib import Path
from filetransfer import Filetransfer
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

class Watcher:

    def __init__(self, metapath=None, watchdir=None, recursive=True):
        while not watchdir:
            watchdir = input("Enter directory to monitor: ")
            if not os.path.exists(watchdir):
                print ("Invalid path")
                watchdir = None

        os.makedirs(os.path.dirname(metapath), exist_ok=True)

        if not os.path.isfile(metapath):
            Path(metapath).touch(exist_ok = True)
    
        self.metafile  = metapath
        self.watchdir  = watchdir
        self.recursive = recursive
        self._started  = False
        

    def scan(self):
        if not self._started:
            self._started = True
            self._newSnap = DirectorySnapshot(path=self.watchdir, recursive=self.recursive)
            self._oldSnap = self._newSnap
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
            
            #Try to open metafile
            with open(self.metafile) as outputfile:
                try:
                    meta = json.load(outputfile)
                except ValueError:
                    meta = {}
                
            if not filename in meta:
                #Push filename in dictionary 
                meta[filename] = {}
                #Creation time
                meta[filename]['timecreated'] = int(time.time())
                #Absolute file path
                meta[filename]['abs_path'] = filepath.replace(self.watchdir, "")

                #Dump into json
                with open(self.metafile, "w") as outputfile:
                    json.dump (meta, outputfile)

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

            with open(self.metafile) as outputfile:
                try:
                    meta = json.load(outputfile)
                except ValueError:
                    meta = {}
                
            #Check if the modified file is in the metafile
            if not filename in meta:
                meta[filename] = {}

            #Add modified timestamp
            meta[filename]['timemodified'] = int(time.time())

            with open(self.metafile, "w") as outputfile:
                json.dump (meta, outputfile)

    def process_files_moved(self):
        for f_old, f_new in self._diffSnap.files_moved:
            oldfile = f_old
            oldname = f_old.split("/")[-1]
            newfile = f_new
            newname = f_new.split("/")[-1]
            print("File moved: {} to {}".format(f_old, f_new))

            with open(self.metafile) as outputfile:
                try:
                    meta = json.load(outputfile)
                except ValueError:
                    meta = {}

            #Check if previous name is known in metafile
            if oldname in meta:
                #Replace the elder with the new
                meta[newname] = meta.pop(oldname)

            #Update modified timestamp
            meta[newname]['timemodified'] = int(time.time())

            with open(self.metafile, "w") as outputfile:
                json.dump(meta, outputfile)

    def process_files_deleted(self):
        for f in self._diffSnap.files_deleted:
            filepath = f
            filename = f.split("/")[-1]
            print("File deleted: {}".format(filename))

            with open(self.metafile) as outputfile:
                try:
                    meta = json.load(outputfile)
                except ValueError:
                    meta = {}
            #Check if file is in metafile
            if filename in meta:
                #Pop from metafile
                meta.pop(filename)
            
            with open(self.metafile, "w") as outputfile:
                json.dump(meta, outputfile)

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
