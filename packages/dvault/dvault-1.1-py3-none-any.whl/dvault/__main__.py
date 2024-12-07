import os

from . import Constants
from . import DBEngine
from . import Operations
from . import Utils
from . import VaultCore


def create_empty_db() -> bool:
    if not (
        os.path.isfile(Constants.VAULT_DB_FILE)
        and os.path.getsize(Constants.VAULT_DB_FILE) != 0
    ):
        Utils.print("Vault is empty, initializing new vault ...")
        open(Constants.VAULT_DB_FILE, "w").close()
        return True
    else:
        return False


def init_db(db_engine: DBEngine, verifier_string: str):
    db_engine.create_tables()
    db_engine.put_reference("version", Constants.APP_VERSION)
    db_engine.put_reference("verifier", verifier_string)
    db_engine.put_reference(Constants.CURR_OBJ, Utils.get_next_object_name())


def verify_password(db_engine: DBEngine, verifier_string: str):
    verifier_string_from_db = db_engine.get_reference("verifier")
    if verifier_string_from_db == verifier_string:
        Utils.print("Password verification success")
    else:
        raise ValueError("Password verification failed")


def menu_loop(vault_core: VaultCore, db_engine: DBEngine):
    operations = Operations(vault_core, db_engine)
    while True:
        option = Utils.input("Do you want to process notes or files (n, f) : ")
        if option == Constants.OPTION_BACK:
            return
        match option:
            case "n":
                entry_type = Constants.ENTRY_TYPE_NOTES
            case "f":
                entry_type = Constants.ENTRY_TYPE_FILES
            case _:
                Utils.print("Invalid option")
                continue
        operations.execute(entry_type)


if __name__ == "__main__":
    db_engine = None
    try:
        # checking for presence of vault
        if not os.path.isdir(Constants.VAULT_DIR):
            raise FileNotFoundError(
                "Vault directory is not present at your home directory\n"
                "Kindly create ~/Vault directory before starting me"
            )

        # if the database is not present or empty, create a new one
        is_new_vault = create_empty_db()

        # take password from user and generate vault core for encryption and decryption
        password = Utils.input_password("Enter the password for vault : ")
        vault_core = VaultCore(password)
        verifier_string = vault_core.encrypt_string("success")

        # creating database engine
        db_engine = DBEngine(Constants.VAULT_DB_FILE)

        # if new vault, create relevant tables in database and insert data
        # else, verify the entered password
        if is_new_vault:
            init_db(db_engine, verifier_string)
        else:
            verify_password(db_engine, verifier_string)

        # welcome prompt and menu loop
        Utils.print(
            f"Welcome to your personal Vault\nEnter {Constants.OPTION_BACK} to go back at any point"
        )
        menu_loop(vault_core, db_engine)

        # exit prompt
        Utils.print("Thank you for using Vault")

    except Exception as e:
        Utils.print(e.args[0])
    except KeyboardInterrupt:
        Utils.print("Interrupted")

    finally:
        # closing the db engine
        if db_engine:
            db_engine.close()
