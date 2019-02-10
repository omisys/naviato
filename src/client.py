# client.py
import os
import getpass
import configparser
from watcher import Watcher


class Client:

    def __init__(self, ip_address, port, uname, dirname):
        self.ip_address = ip_address
        self.port = port
        self.uname = uname
        self.dirname = dirname

    @staticmethod
    def read_config():
        print(os.getegid())

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


def get_home_dir():
    return os.path.join("/home", getpass.getuser())


def read_config():
    # get the absolute path to the config file (can run client.py from anywhere)
    abs_file_path = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(abs_file_path, "../config")

    # read config file
    config = configparser.RawConfigParser()
    config.read(config_path)

    # print some parameters
    seperator = ":"
    address = (config.get('example-config', 'ip'), config.get('example-config', 'port'))
    print(seperator.join(address))


def main():
    print(getpass.getuser())
    read_config()
    testclient = Client("192.168.0.1", 1234, getpass.getuser(), None)
    # testclient.get_public_key()
    testclient.dirname = input("Enter directory to monitor: ")
    w = Watcher(testclient.dirname)
    w.run()


if __name__ == "__main__":
    main()
