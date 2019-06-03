import os
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.settings_module"


""" Library is redundant at the moment. """


def handle_uploaded_file(path):
    """ Function saves uploaded file to storage. """
    with open(f"{path}", "wb+") as destination:
        for chunk in path.chunks():
            default_storage.save(f"user/documents/new_file_{path}", ContentFile(chunk))


class NativeFile:
    """ NativeFile.file represents django file object. """

    def __init__(self, path):
        """ Path (string) from MEDIA_ROOT to file or just file name."""
        self.path = path
        self.file = self.file_object_creates()
        self.save_to_storage()

    def open_file_from_dir(self):
        """ Opens file from direction. """
        # settings.MEDIA_ROOT deleted to make method universal.
        return open(self.path, "wb+")

    def file_object_creates(self):
        """ Creates File instance. """
        return File(self.open_file_from_dir())

    def save_to_storage(self):
        return default_storage.save(
            f"user/documents/new", ContentFile(self.file.read())
        )


# obj_file = NativeFile('test_root.txt')

# obj content \/
# print(obj_file.file.read())
# path = default_storage.save('path/to/nowy_file.txt', ContentFile(obj_file.file.read()))


# image_obj = NativeFile('piesek.jpg')
# image content\/
# print(image_obj.file.read())
# image = default_storage.save('path/to/piesek.jpg', ContentFile(image_obj.file.read()))
