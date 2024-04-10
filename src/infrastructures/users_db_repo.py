from entities.users_db_interface import IUsersDBRepository

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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_email TEXT NOT NULL,
    FOREIGN KEY (parent_email) REFERENCES parents(email)
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
GET_CHILDREN = """
SELECT * FROM children
"""
ADD_CHILD = """
INSERT INTO children (name, parent_email)
VALUES (?, ?)
"""
GET_CHILD = """
SELECT * FROM children WHERE id = ?
"""
UPDATE_CHILD = """
UPDATE children SET name = ? WHERE id = ?
"""
REMOVE_CHILD = """
DELETE FROM children WHERE id = ?
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
        if self.get_parent(parent.email):
            return
        
        self.cursor.execute(ADD_PARENT, (parent.email, parent.name, parent.get_password_hash()))
        self.connection.commit()

    def get_parents(self):
        self.cursor.execute(GET_PARENTS)
        return self.cursor.fetchall()
    
    def get_parent(self, email):
        self.cursor.execute(GET_PARENT, (email,))
        self.cursor.fetchone()

    def update_parent(self, parent):
        self.cursor.execute(UPDATE_PARENT, (parent.new_name, parent.email))
        self.connection.commit()

    def add_child(self, child):
        self.cursor.execute(ADD_CHILD, (child.name, child.parent_email))
        self.connection.commit()

    def get_children(self):
        self.cursor.execute(GET_CHILDREN)
        return self.cursor.fetchall()
    
    def get_child(self, child_id):
        self.cursor.execute(GET_CHILD, (child_id,))
        return self.cursor.fetchone()
    
    def update_child(self, child):
        self.cursor.execute(UPDATE_CHILD, (child.new_name, child.id))
        self.connection.commit()

    def remove_child(self, child):
        self.cursor.execute(REMOVE_CHILD, (child.id,))
        self.connection.commit()

    def remove_parent(self, parent):
        self.cursor.execute(REMOVE_PARENT, (parent.email,))
        self.connection.commit()