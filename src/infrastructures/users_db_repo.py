from entities.users_db_interface import IUsersDBRepository

import sqlite3

class UsersDBRepository(IUsersDBRepository):
    """
    Implementation of the users database repository with sqlite3.
    """

    PEPPER = b'some_random_pepper'

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS parents (
                email TEXT PRIMARY KEY NOT NULL,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS children (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER NOT NULL,
                FOREIGN KEY (parent_id) REFERENCES parents (id)
            )
            """
        )
        self.connection.commit()

    def add_parent(self, parent):
        self.cursor.execute(
            """
            INSERT INTO parents (email, username, password_hash)
            VALUES (?, ?, ?)
            """,
            (parent.email, parent.name, parent.get_password_hash())
            )
        self.connection.commit()

    def get_parents(self):
        self.cursor.execute(
            """
            SELECT * FROM parents
            """
        )
        return self.cursor.fetchall()
    
    def add_child(self, child):
        self.cursor.execute(
            """
            INSERT INTO children (name, parent_id)
            VALUES (?, ?)
            """,
            (child.name, child.parent_id)
        )
        self.connection.commit()

    def get_children(self, parent_id):
        self.cursor.execute(
            """
            SELECT * FROM children WHERE parent_id = ?
            """,
            (parent_id,)
        )
        return self.cursor.fetchall()
    