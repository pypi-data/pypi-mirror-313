import os


class Constants:
    APP_VERSION = "1.0"
    MY_BIRTH_DAY_UNIX_SECONDS = 860201400
    MY_BIRTH_DAY_BYTE_ARRAY = b"05 April 1997 AD"
    SALT = b"\x18\xec7$\xd9\x85\xc87$i\xa3\xfeZ-\xd49\xe2\xb1$\x11\xc3C\xe5\xf1\xc0\xf8\x136%\xd7\xcd!"
    VAULT_DIR = os.path.join(os.getenv("USERPROFILE"), "Vault")
    VAULT_DB_FILE = os.path.join(VAULT_DIR, "master.db")
    OBJ_NAME_LEN = 8
    ENTRY_TYPE_NOTES = "Notes"
    ENTRY_TYPE_FILES = "Files"
    OPTION_BACK = "!"
    CURR_OBJ = "curr_obj"

    ERR_DECRYPT = "DECRYPT"
    ERR_SQLITE_BUSY = "SQLITE_BUSY"
    ERR_SQLITE_CONSTRAINT_UNIQUE = "SQLITE_CONSTRAINT_UNIQUE"
    ERR_SQLITE_NO_DATA_FOUND = "NO_DATA_FOUND"
    ERR_SQLITE_FATAL = (
        "Fatal error occurred while accessing database, most likely due to corruption.\n"
        "Kindly delete all files present in ~/Vault as they are tampered"
    )

    ERR_FILE_MISSING = "FILE_MISSING"
    ERR_OBJ_MISSING = "OBJ_MISSING"
    ERR_NO_PERMISSIONS = "NO_PERMISSIONS"
