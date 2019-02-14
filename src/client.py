# client.py
import os
import getpass
import configparser
from watcher import Watcher


class Client:
    CHUNK_SIZE = 1024

    def __init__(self, conf_path):
        # get the absolute path to the current directory
        self.abs_file_path = os.path.abspath(os.path.dirname(__file__))
        self.config_path = os.path.join(self.abs_file_path, conf_path)
        self.read_config()

    def read_config(self):
        # read config file
        config = configparser.RawConfigParser()
        config.read(self.config_path)
        self.host = config.get('example-config', 'host')
        self.port = config.get('example-config', 'port')

    def get_home_dir():
        return os.path.join("/home", getpass.getuser())

    @staticmethod
    def get_public_key():
        # find public SSH key
        pubkey = None
        pubkey_dirname = os.path.join(get_home_dir(), ".ssh")

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
    print(getpass.getuser())
    print(os.getegid())
    testclient = Client("../config")
    # testclient.get_public_key()
    testclient.dirname = input("Enter directory to monitor: ")
    w = Watcher(testclient.dirname)
    w.run()


if __name__ == "__main__":
    main()
