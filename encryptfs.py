import os
import json

from encrypt_files import decrypt_file, encrypt_file, gen_key

def index_path(directory):
    return os.path.join(directory, 'index.json')

def index_path_enc(directory):
    return os.path.join(directory, 'index.json.enc')

class EncryptFS:
    def __init__(self, password, starting_dir=None):
        self.key = gen_key(password)
        self.current_dir = starting_dir if starting_dir else './'

    def list_dir(self, directory=None):
        if not directory:
            directory = self.current_dir

        # init index if necessary
        if not os.path.isfile(index_path_enc(directory)):
            with open(index_path(directory), 'wb') as outfile:
                outfile.write("{}")
            encrypt_file(self.key, index_path(directory))
            os.remove(index_path(directory))

        # TODO: bypass temp file
        # TODO: use cStringIO to decrypt straight to memory
        decrypt_file(self.key, index_path_enc(directory))
        with open(index_path(directory), 'rb') as file:
            index = json.load(file)
        print index