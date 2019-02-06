# client.py
import os

class Client():

    def __init__(self, ip_address, port, uname, dir):
        self.ip_address = ip_address
        self.port = port
        self.uname = uname
        self.dir = dir

    def get_public_key(self):
        #find public SSH key
        pubkey = None
        pubkey_dirname = os.path.join("/home", self.uname, ".ssh")
        
        print("Pub key directory:", pubkey_dirname)

        for tuple in os.walk(pubkey_dirname):
            dirname, dirnames, filenames = tuple
            break

        for filename in filenames:
            if '.pub' in filename:
                pubkey_filepath = os.path.join(dirname, filename)
                print("Pub key file:", pubkey_filepath)
                pubkey = open(pubkey_filepath, 'r').readline()
                print("Pub key:", pubkey)
        return pubkey
    

def main():
    testClient = Client("192.168.0.1", 1234, "jop", None)
    testClient.get_public_key()

if __name__ == "__main__":
    main()
