from entities.users_db_interface import IUsersDBRepository
from ServerAPI.shared.SharedDTO import ParentData
import sqlite3
import datetime
import hashlib

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
ADD_AGENT = """
INSERT INTO agents (auth_string, mac_address, time_stamp)
VALUES (?, ?, ?)
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

    def new_agent(self, mac_address):
        time = datetime.datetime.now()
        auth_string = hashlib.sha256(mac_address.encode() + str(time).encode()).hexdigest()[:8]
        self.cursor.execute(ADD_AGENT, (auth_string, mac_address, str(time)))
        self.connection.commit()
        return auth_string
    
    def confirm_agent(self, parent_email, auth_string):
        self.cursor.execute("SELECT * FROM agents WHERE auth_string = ?", (auth_string,))
        agent = self.cursor.fetchone()
        if agent is None:
            return False
        # if more than 5 minutes have passed since the agent was created, it is invalid
        time = datetime.datetime.now()
        agent_time = datetime.datetime.strptime(agent[2], "%Y-%m-%d %H:%M:%S.%f")
        if (time - agent_time).seconds > 300:
            return False

        # generate child_id
        self.cursor.execute("SELECT * FROM children")
        children = self.cursor.fetchall()
        child_id = len(children) + 1

        self.cursor.execute("INSERT INTO children (child_id, auth_string, mac_address, parent_email) VALUES (?, ?, ?, ?)", (child_id, auth_string, agent[1], parent_email))
        self.connection.commit()
        return True
    
    def get_child_id(self, auth_string):
        self.cursor.execute("SELECT * FROM children WHERE auth_string = ?", (auth_string,))
        child = self.cursor.fetchone()
        if child is None:
            return None
        return child[0]


