import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Native_Service.settings_module'

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class NativeFile:
    """ NativeFile.file represents django file object. """

    def __init__(self, path):
        """ Path (string) from MEDIA_ROOT to file or just file name."""
        self.path = path
        self.file = self.file_object_creates()

    def open_file_from_dir(self):
        """ Opens file from direction. """
        return open(settings.MEDIA_ROOT + self.path, 'rb')


    def file_object_creates(self):
        """ Creates File instance. """
        return File(self.open_file_from_dir())




"""

obj_file = NativeFile('test_root.txt')

# obj content \/
print(obj_file.file.read())
#path = default_storage.save('path/to/nowy_file.txt', ContentFile(obj_file.file.read()))


image_obj = NativeFile('piesek.jpg')
# image content\/
print(image_obj.file.read())
#image = default_storage.save('path/to/piesek.jpg', ContentFile(image_obj.file.read()))

"""