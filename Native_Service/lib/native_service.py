import os
import sys


class NativeFile:
    """ Creates an object assigned to file."""

    def __init__(self, patch, type, name, file_extension, size):
        self.patch = patch
        self.type = type
        self.name = name
        self.file_extension = file_extension
        self.size = size

    def _patch(self):
        # hmm
        patch = self.patch
        os.getcwd()
        start_point = 0
        file = os.open('../LICENSE', os.O_RDWR| os.O_CREAT)
        return os.read(file, 12)


    def _save(self):
        pass

    def _open(self):
        pass

    def _get_url(self):
        pass


file = NativeFile(1,2,3,4,5)
print(file._patch())