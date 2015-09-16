import os
import json

from encrypt_files import decrypt_file, encrypt_file, gen_key

# TODO: move this to a config later
ignored_files = [
    '.DS_Store'
]

def index_path(directory):
    return os.path.join(directory, 'index.json')

def index_path_enc(directory):
    return os.path.join(directory, 'index.json.enc')

def empty_index(directory):
    return {
        "files": []
    }

def enc_filenames_for_index(index):
    filenames = []
    for f in index["files"]:
        filenames.append(f["filename_enc"])
    return filenames

def encrypt_and_remove_original(key, path, out_path=None):
        encrypt_file(key, path, out_filename=out_path)
        os.remove(path)

def gen_random_filename():
    return os.urandom(32).encode('hex')

class EncryptFS:
    def __init__(self, password, starting_dir=None):
        self.key = gen_key(password)
        self.current_dir = starting_dir if starting_dir else './'
        self.current_index = self.load_index()

    def load_index(self, directory=None):
        if not directory:
            directory = self.current_dir

        # init index if new dir
        if not os.path.isfile(index_path_enc(directory)):
            self.update_index(directory=directory)
            return empty_index(directory)

        # TODO: bypass temp file
        # TODO: use cStringIO to decrypt straight to memory
        decrypt_file(self.key, index_path_enc(directory))
        with open(index_path(directory), 'rb') as file:
            index = json.load(file)
        os.remove(index_path(directory))
        
        return index

    def update_index(self, index=None, directory=None):
        if not directory:
            directory = self.current_dir

        if not index:
            index = empty_index(directory)

        with open(index_path(directory), 'w') as outfile:
            json.dump(index, outfile)
        encrypt_and_remove_original(self.key, index_path(directory))

    def add_file_to_index(self, filename, filename_enc):
        self.current_index["files"].append({
            "filename": filename,
            "filename_enc": filename_enc
        })

    def encrypt_all(self, directory=None):
        if not directory:
            directory = self.current_dir

        in_index = enc_filenames_for_index(self.current_index)
        not_indexed = [f for f in os.listdir(directory) if (
                        (not f in in_index) and
                        (not f in ignored_files) and
                        (f != 'index.json.enc') and
                        os.path.isfile(os.path.join(directory, f)))]

        for f in not_indexed:
            out_name = gen_random_filename()
            encrypt_and_remove_original(self.key, os.path.join(directory, f), out_path=os.path.join(directory, out_name))
            self.add_file_to_index(f, out_name)

        self.update_index(index=self.current_index, directory=directory)

    def default_if_necessary(self, directory=None, index=None):
        if not directory and not index:
            directory = self.current_dir
            index = self.current_index
        elif (not directory and index) or (directory and not index):
            raise RuntimeError("Must pass both directory or index or neither")
        return directory, index

    def decrypt_all(self, directory=None, index=None, delete_encrypted=False):
        directory, index = self.default_if_necessary(directory, index)

        # TODO: stop depending on some self vars and not others
        # probably separate logic from instance vars with static methods?
        for file in index["files"]:
            decrypt_file(self.key, os.path.join(directory, file["filename_enc"]), out_filename=os.path.join(directory, file["filename"]))
            if delete_encrypted:
                os.remove(os.path.join(directory, file["filename_enc"]))

    def prune_index(self, directory=None, index=None):
        """ Removes deleted files from the index.
            Does not affect index.
        """
        directory, index = self.default_if_necessary(directory, index)

        for file in index:
            filepath = os.path.join(directory, file["filename_enc"])
            if not os.path.isfile(filepath):
                os.remove(filepath)