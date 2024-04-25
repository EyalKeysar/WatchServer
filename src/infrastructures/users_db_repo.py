from entities.users_db_interface import IUsersDBRepository
from ServerAPI.shared.SharedDTO import ParentData
import sqlite3

CREATE_PARENTS_TABLE = """
CREATE TABLE IF NOT EXISTS parents (
    email TEXT PRIMARY KEY NOT NULL,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
)
"""
CREATE_CHILDREN_TABLE = """
CREATE TABLE IF NOT EXISTS children (
    child_id INTEGER PRIMARY KEY,
    parent_email TEXT REFERENCES parents(email),
    name TEXT NOT NULL
)
"""
ADD_PARENT = """
INSERT INTO parents (email, username, password_hash)
VALUES (?, ?, ?)
"""
GET_PARENTS = """
SELECT * FROM parents
"""
GET_PARENT = """
SELECT * FROM parents WHERE email = ?
"""
UPDATE_PARENT = """
UPDATE parents SET username = ? WHERE email = ?
"""
REMOVE_PARENT = """
DELETE FROM parents WHERE email = ?
"""

class UsersDBRepository(IUsersDBRepository):
    """
    Implementation of the users database repository with sqlite3.
    """

    PEPPER = b'some_random_pepper'

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_PARENTS_TABLE)
        self.cursor.execute(CREATE_CHILDREN_TABLE)
        self.connection.commit()

    def add_parent(self, parent):
        if self.get_parent(parent.email) is not None:
            return False
        self.cursor.execute(ADD_PARENT, (parent.email, parent.name, parent.password_hash))
        self.connection.commit()
        return True

    def get_parents(self):
        self.cursor.execute(GET_PARENTS)
        return self.cursor.fetchall()
    
    def get_parent(self, email):
        self.cursor.execute(GET_PARENT, (email,))
        str_parent = self.cursor.fetchone()
        if str_parent is None:
            return None
        return ParentData(str_parent[0], str_parent[1], str_parent[2])


    def update_parent(self, parent):
        self.cursor.execute(UPDATE_PARENT, (parent.new_name, parent.email))
        self.connection.commit()

    def remove_parent(self, parent):
        self.cursor.execute(REMOVE_PARENT, (parent.email,))
        self.connection.commit()