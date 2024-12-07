import sqlite3

from . import Constants


class DBEngine:
    def __init__(self, db_file: str):
        self.__db_connection = sqlite3.connect(db_file)
        self.__db_cursor = self.__db_connection.cursor()

    def create_tables(self):
        self.__db_cursor.execute(
            "CREATE TABLE reference (name TEXT PRIMARY KEY, value TEXT)"
        )
        self.__db_cursor.execute(
            "CREATE TABLE files (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT, "
            "UNIQUE(name, type)"
            ")"
        )
        self.__db_cursor.execute(
            "CREATE TABLE objects (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id INTEGER, page INTEGER, name TEXT UNIQUE, "
            "FOREIGN KEY(file_id) REFERENCES files(id)"
            ")"
        )

    def __execute_without_commit(
        self, query: str, params: tuple = ()
    ) -> sqlite3.Cursor:
        try:
            result_cursor = self.__db_cursor.execute(query, params)
            return result_cursor
        except sqlite3.Error:
            raise RuntimeError(Constants.ERR_SQLITE_FATAL)

    def __execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        try:
            result_cursor = self.__db_cursor.execute(query, params)
            self.__db_connection.commit()
            return result_cursor
        except sqlite3.Error as e:
            if e.sqlite_errorname in [
                Constants.ERR_SQLITE_CONSTRAINT_UNIQUE,
                Constants.ERR_SQLITE_BUSY,
            ]:
                raise RuntimeError(e.sqlite_errorname)
            else:
                raise RuntimeError(Constants.ERR_SQLITE_FATAL)

    def __get_objects(self, file_id: str) -> list[tuple]:
        raw_data = self.__execute_without_commit(
            "SELECT id, page, name FROM objects WHERE file_id = ?", (file_id,)
        ).fetchall()
        return [(entry[0], entry[2]) for entry in raw_data]

    def __get_note_id(self, enc_name: str) -> str:
        result = self.__execute_without_commit(
            "SELECT id FROM files WHERE type = 'note' AND name = ?", (enc_name,)
        ).fetchone()

        if result is None:
            raise RuntimeError(Constants.ERR_SQLITE_NO_DATA_FOUND)
        else:
            return result[0]

    def __get_file_id(self, enc_name: str) -> str:
        result = self.__execute_without_commit(
            "SELECT id FROM files WHERE type = 'file' AND name = ?", (enc_name,)
        ).fetchone()

        if result is None:
            raise RuntimeError(Constants.ERR_SQLITE_NO_DATA_FOUND)
        else:
            return result[0]

    def __insert_object(self, file_id: str, obj_name: str):
        self.__execute(
            "INSERT INTO objects(file_id, page, name) VALUES(?, ?, ?)",
            (file_id, 0, obj_name),
        )

    def get_reference(self, name: str):
        result = self.__execute_without_commit(
            "SELECT value FROM reference WHERE name = ?", (name,)
        ).fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def put_reference(self, name: str, value):
        if self.get_reference(name) is None:
            self.__execute(
                "INSERT INTO reference(name, value) VALUES(?, ?)", (name, value)
            )
        else:
            self.__execute(
                "UPDATE reference SET value = ? WHERE name = ?", (value, name)
            )

    def get_notes(self):
        return self.__execute_without_commit(
            "SELECT id, name FROM files WHERE type = 'note'"
        ).fetchall()

    def get_files(self):
        return self.__execute_without_commit(
            "SELECT id, name FROM files WHERE type = 'file'"
        ).fetchall()

    def get_note_objects(self, enc_name: str) -> list[tuple]:
        note_id = self.__get_note_id(enc_name)
        return self.__get_objects(note_id)

    def insert_note_and_objects(self, enc_name: str, obj_name: str):
        self.__execute("INSERT INTO files(name, type) VALUES(?, 'note')", (enc_name,))
        note_id = self.__get_note_id(enc_name)
        self.__insert_object(note_id, obj_name)

    def get_file_objects(self, enc_name: str) -> list[tuple]:
        file_id = self.__get_file_id(enc_name)
        return self.__get_objects(file_id)

    def insert_file_and_objects(self, enc_name: str, obj_name: str):
        self.__execute("INSERT INTO files(name, type) VALUES(?, 'file')", (enc_name,))
        file_id = self.__get_file_id(enc_name)
        self.__insert_object(file_id, obj_name)

    def delete_note(self, enc_name: str):
        self.__execute(
            "DELETE FROM files WHERE type = 'note' AND name = ?", (enc_name,)
        )

    def delete_file(self, enc_name: str):
        self.__execute(
            "DELETE FROM files WHERE type = 'file' AND name = ?", (enc_name,)
        )

    def delete_object(self, object_id: str):
        self.__execute("DELETE FROM objects WHERE id = ?", (object_id,))

    def rollback(self):
        self.__db_connection.rollback()

    def close(self):
        self.__db_cursor.close()
        self.__db_connection.close()
