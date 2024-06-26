from entities.users_db_interface import IUsersDBRepository
from ServerAPI.shared.SharedDTO import ParentData
import sqlite3
import hashlib

# SQL queries for table creation
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
    auth_string TEXT,
    mac_address TEXT NOT NULL,
    parent_email TEXT REFERENCES parents(email)
)
"""
CREATE_AGENTS_TABLE = """
CREATE TABLE IF NOT EXISTS agents (
    auth_string TEXT PRIMARY KEY NOT NULL,
    mac_address TEXT NOT NULL,
    time_stamp TEXT NOT NULL
)
"""

# SQL queries for parents operations
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

# SQL queries for agents operations
ADD_AGENT = """
INSERT INTO agents (auth_string, mac_address, time_stamp)
VALUES (?, ?, ?)
"""
GET_WAITING_AGENT = """
SELECT * FROM agents WHERE auth_string = ?
"""
DELETE_WAITING_AGENT = """
DELETE FROM agents WHERE auth_string = ?
"""

# SQL queries for children operations
ADD_CHILD = """
INSERT INTO children (child_id, auth_string, mac_address, parent_email)
VALUES (?, ?, ?, ?)
"""
GET_ALL_CHILDREN = """
SELECT * FROM children
"""
GET_AGENT = """
SELECT * FROM children WHERE auth_string = ?
"""
GET_CHILD_ID_BY_MAC = """
SELECT child_id FROM children WHERE mac_address = ?
"""
GET_MAC_ADDR = """
SELECT mac_address FROM children WHERE parent_email = ? AND child_id = ?
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
        self.cursor.execute(CREATE_AGENTS_TABLE)
        self.connection.commit()

    def add_parent(self, parent):
        # Check if parent already exists
        if self.get_parent(parent.email)[1] is not None:
            return False
        # Add new parent
        self.cursor.execute(ADD_PARENT, (parent.email, parent.name, parent.password_hash))
        self.connection.commit()
        return True
    
    def get_parent(self, email):
        self.cursor.execute(GET_PARENT, (email,))
        str_parent = self.cursor.fetchone()
        if str_parent is None:
            return False, None, None
        return True, str_parent[1], str_parent[2]

    def update_parent(self, parent):
        self.cursor.execute(UPDATE_PARENT, (parent.new_name, parent.email))
        self.connection.commit()

    def remove_parent(self, parent):
        self.cursor.execute(REMOVE_PARENT, (parent.email,))
        self.connection.commit()

    def new_agent(self, mac_address, current_time, auth_string):
        self.cursor.execute(ADD_AGENT, (auth_string, mac_address, current_time))
        self.connection.commit()
        return True
    
    def get_time_stamp(self, auth_string):
        self.cursor.execute(GET_WAITING_AGENT, (auth_string,))
        agent = self.cursor.fetchone()
        if agent is None:
            return None
        return agent[2]
    
    def get_waiting_agent_mac_address(self, auth_string):
        self.cursor.execute(GET_WAITING_AGENT, (auth_string,))
        agent = self.cursor.fetchone()
        if agent is None:
            return None
        return agent[1]
    
    def remove_waiting_agent(self, auth_string):
        self.cursor.execute(DELETE_WAITING_AGENT, (auth_string,))
        self.connection.commit()

    def get_all_children(self):
        self.cursor.execute(GET_ALL_CHILDREN)
        return self.cursor.fetchall()

    def add_child(self, mac_address, parent_email, auth_string, child_id):
        self.cursor.execute(ADD_CHILD, (child_id, auth_string, mac_address, parent_email))
        self.connection.commit()
        return True
    
    def get_agent(self, auth_string):
        self.cursor.execute(GET_AGENT, (auth_string,))
        agent = self.cursor.fetchone()
        if agent is None:
            return False, None
        return True, agent[2]
    
    def get_child_id_by_mac(self, mac_address):
        self.cursor.execute(GET_CHILD_ID_BY_MAC, (mac_address,))
        child_id = self.cursor.fetchone()
        if child_id is None:
            return None
        return child_id[0]

    def get_mac_addr(self, email, child_id):
        self.cursor.execute(GET_MAC_ADDR, (email, child_id))
        mac_address = self.cursor.fetchone()
        if mac_address is None:
            return None
        return mac_address[0]
