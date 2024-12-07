import os

from . import Constants
from . import DBEngine
from . import FileInterface
from . import Utils
from . import VaultCore


class Operations:
    def __init__(self, vault_core: VaultCore, db_engine: DBEngine):
        self.vault_core = vault_core
        self.db_engine = db_engine
        self.file_interface = FileInterface()

    def execute(self, entry_type: str):
        method_to_use = (
            self.db_engine.get_notes
            if entry_type == Constants.ENTRY_TYPE_NOTES
            else self.db_engine.get_files
        )
        while True:
            list_of_entries = {
                id: self.vault_core.decrypt_string(enc_name)
                for id, enc_name in method_to_use()
            }
            Utils.print(entry_type + " present in the vault :")
            Utils.print_list(list(list_of_entries.values()))

            option = Utils.input("Do you want to read/write or delete (r, w, d) : ")
            if option == Constants.OPTION_BACK:
                return
            entry_name = Utils.input("Enter name : ")
            self.try_and_handle_exceptions(option, entry_type, entry_name)

    def try_and_handle_exceptions(self, option: str, entry_type: str, entry_name: str):
        try:
            match option:
                case "r":
                    self.execute_r(entry_type, entry_name)
                case "w":
                    self.execute_w(entry_type, entry_name)
                case "d":
                    self.execute_d(entry_type, entry_name)
                case _:
                    Utils.print("Invalid option")
        except RuntimeError as re:
            match re.args[0]:
                case Constants.ERR_SQLITE_BUSY:
                    Utils.print("Master db is locked")
                    self.db_engine.rollback()
                case Constants.ERR_SQLITE_NO_DATA_FOUND:
                    Utils.print("Entry does not exist")
                case Constants.ERR_SQLITE_CONSTRAINT_UNIQUE:
                    Utils.print("Entry already exists")
                case Constants.ERR_DECRYPT:
                    Utils.print("Object looks corrupted, kindly delete the entry")
                case Constants.ERR_OBJ_MISSING:
                    Utils.print("Object is missing, kindly delete the entry")
                case Constants.ERR_FILE_MISSING:
                    Utils.print("File does not exist")
                case Constants.ERR_NO_PERMISSIONS:
                    Utils.print("No permissions to create/delete files")
                case _:
                    raise

    def execute_r(self, message: str, entry_name: str):
        if entry_name == Constants.OPTION_BACK:
            return
        if message == Constants.ENTRY_TYPE_NOTES:
            self.read_note(entry_name)
        else:
            self.read_file(entry_name)

    def execute_w(self, message: str, entry_name: str):
        if entry_name == Constants.OPTION_BACK:
            return
        entry_location = Utils.input("Enter location : ")
        if entry_location == Constants.OPTION_BACK:
            return
        if message == Constants.ENTRY_TYPE_NOTES:
            self.write_note(entry_name, entry_location)
        else:
            self.write_file(entry_name, entry_location)

    def execute_d(self, message: str, entry_name: str):
        if entry_name == Constants.OPTION_BACK:
            return
        if message == Constants.ENTRY_TYPE_NOTES:
            self.del_note(entry_name)
        else:
            self.del_file(entry_name)

    def read_generic(self, entry_name: str, db_read_method) -> bytes:
        enc_name = self.vault_core.encrypt_string(entry_name)
        objects = db_read_method(enc_name)

        obj_array = b""
        for object in objects:
            obj_array += self.file_interface.read_object(object[1])

        return self.vault_core.decrypt_bytes(obj_array)

    def write_generic(self, entry_name: str, file_data: bytes, db_write_method):
        obj_name = self.db_engine.get_reference(Constants.CURR_OBJ)
        self.file_interface.write_object(
            obj_name, self.vault_core.encrypt_bytes(file_data)
        )

        enc_name = self.vault_core.encrypt_string(entry_name)
        db_write_method(enc_name, obj_name)
        self.db_engine.put_reference(
            Constants.CURR_OBJ, Utils.get_next_object_name(obj_name)
        )

    def delete_generic(self, entry_name: str, db_read_method, db_del_method):
        enc_name = self.vault_core.encrypt_string(entry_name)
        objects = db_read_method(enc_name)

        for object in objects:
            self.db_engine.delete_object(object[0])
            self.file_interface.delete_object(object[1])

        db_del_method(enc_name)

    def read_note(self, entry_name: str):
        dec_obj_array = self.read_generic(entry_name, self.db_engine.get_note_objects)
        print(dec_obj_array.decode())

    def write_note(self, entry_name: str, entry_location: str):
        file_data = self.file_interface.read_file(entry_location, entry_name)
        self.write_generic(
            entry_name, file_data, self.db_engine.insert_note_and_objects
        )

    def del_note(self, entry_name: str):
        self.delete_generic(
            entry_name, self.db_engine.get_note_objects, self.db_engine.delete_note
        )

    def read_file(self, entry_name: str):
        dest_location = Utils.input("Enter location : ")
        if dest_location == Constants.OPTION_BACK:
            return
        if not os.path.isdir(dest_location):
            Utils.print("Given destination does not exist")
            return
        if os.path.isfile(os.path.join(dest_location, entry_name)):
            response = Utils.input(
                "File already exists, do you want to override (y, n) : "
            )
            if response in [Constants.OPTION_BACK, "n"]:
                return

        dec_obj_array = self.read_generic(entry_name, self.db_engine.get_file_objects)
        self.file_interface.write_file(dest_location, entry_name, dec_obj_array)

    def write_file(self, entry_name: str, entry_location: str):
        file_data = self.file_interface.read_file(entry_location, entry_name)
        self.write_generic(
            entry_name, file_data, self.db_engine.insert_file_and_objects
        )

    def del_file(self, entry_name: str):
        self.delete_generic(
            entry_name, self.db_engine.get_file_objects, self.db_engine.delete_file
        )
