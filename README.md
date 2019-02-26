# Naviato
![](https://raw.githubusercontent.com/omisys/new_aviato/master/naviato.png)

File sync for Stallions

## To do

### General
- [ ] secure file transfer
- [x] auto sync
- [x] file transfer in blocks

### Server
- [ ] server configuration tool
- [x] accept incoming connections
- [ ] parse metadata file
- [ ] download missing files from client
- [ ] upload missing files to client

### Client
- [x] read config file
- [ ] command line client interface
- [x] upload files to server

### File watcher
- [x] recognize file changes in directory
- [ ] upload metadata on every change to file using client connection
- [ ] make recent changes available to user

### Metadata
- [ ] generate unique file ID
- [x] create metadata file on first detection of file
- [x] update metadata on change
- [ ] determine content of meta data file
eg:
```
{
    "dateClientModified" : 1234,
    "dateServerModified" : 1234,
    "fileSize" : 1234,
    "revision" : 0
}
```

