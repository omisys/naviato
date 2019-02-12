# Naviato
![](https://raw.githubusercontent.com/omisys/new_aviato/master/naviato.png)

File sync for Stallions

## To do

### General
- [ ] secure file transfer
- [ ] auto sync
- [ ] file transfer in blocks

### Client
- [x] read config file
- [ ] command line client interface
- [ ] upload files to server

### File watcher
- [x] recognize file changes in directory
- [ ] upload metadata on every change to file using client connection
- [ ] make recent changes available to user

### Server
- [ ] server configuration tool
- [ ] accept incoming connections
- [ ] parse metadata file
- [ ] download missing files from client
- [ ] upload missing files to client

### Metadata
- [ ] generate unique file ID
- [ ] create metadata file on first detection of file
- [ ] update metadata on change
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

