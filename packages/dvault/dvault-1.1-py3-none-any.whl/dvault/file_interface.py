import os

from . import Constants


class FileInterface:
    def __read(self, file: str, is_obj: bool) -> bytes:
        try:
            with open(file, "rb") as file:
                return file.read()
        except FileNotFoundError:
            raise RuntimeError(
                Constants.ERR_OBJ_MISSING if is_obj else Constants.ERR_FILE_MISSING
            )

    def __write(self, file: str, data: bytes):
        try:
            with open(file, "wb") as obj_file:
                obj_file.write(data)
        except PermissionError:
            raise RuntimeError(Constants.ERR_NO_PERMISSIONS)

    def read_object(self, obj_name: str) -> bytes:
        return self.__read(os.path.join(Constants.VAULT_DIR, obj_name), True)

    def write_object(self, obj_name: str, obj_data: bytes):
        self.__write(os.path.join(Constants.VAULT_DIR, obj_name), obj_data)

    def delete_object(self, obj_name: str):
        object_file = os.path.join(Constants.VAULT_DIR, obj_name)
        try:
            if os.path.isfile(object_file):
                os.remove(object_file)
        except PermissionError:
            raise RuntimeError(Constants.ERR_NO_PERMISSIONS)

    def read_file(self, entry_location: str, entry_name: str) -> bytes:
        return self.__read(os.path.join(entry_location, entry_name), False)

    def write_file(self, dest_location: str, entry_name: str, file_data: bytes):
        self.__write(os.path.join(dest_location, entry_name), file_data)
