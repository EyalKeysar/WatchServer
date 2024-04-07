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
                FOREIGN KEY (parent_email) REFERENCES parents(email)
            )
            """
        )
        self.connection.commit()

    def add_parent(self, parent):
        # Check if parent already exists
        if self.get_parent(parent.email):
            return

        # Add parent
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
    
    def get_parent_by_email(self, email):
        self.cursor.execute(
            """
            SELECT * FROM parents WHERE email = ?
            """,
            (email,)
        )
        self.cursor.fetchone()
        

    def update_parent(self, parent):
        self.cursor.execute(
            """
            UPDATE parents SET username = ? WHERE email = ?
            """,
            (parent.new_name, parent.email)
        )
        self.connection.commit()

    def add_child(self, child):
        self.cursor.execute(
            """
            INSERT INTO children (name, parent_email)
            VALUES (?, ?)
            """,
            (child.name, child.parent_email)
        )
        self.connection.commit()

    def get_children(self):
        self.cursor.execute(
            """
            SELECT * FROM children
            """
        )
        return self.cursor.fetchall()
    
    def get_child(self, child_id):
        self.cursor.execute(
            """
            SELECT * FROM children WHERE id = ?
            """,
            (child_id,)
        )
        return self.cursor.fetchone()
    
    def update_child(self, child):
        self.cursor.execute(
            """
            UPDATE children SET name = ? WHERE id = ?
            """,
            (child.new_name, child.id)
        )
        self.connection.commit()

    def delete_child(self, child_id):
        self.cursor.execute(
            """
            DELETE FROM children WHERE id = ?
            """,
            (child_id,)
        )
        self.connection.commit()



    def remove_child(self, child, parent):
        self.cursor.execute(
            """
            DELETE FROM children WHERE id = ? AND parent_email = ?
            """,
            (child.id, parent.email)
        )
        self.connection.commit()

    def remove_parent(self, parent):
        self.cursor.execute(
            """
            DELETE FROM parents WHERE email = ?
            """,
            (parent.email,)
        )
        self.connection.commit()



    