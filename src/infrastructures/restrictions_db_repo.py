from entities.restrictions_db_interface import IRestrictionsDBRepository

import sqlite3

CREATE_RESTRICTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS restrictions (
    id INTEGER PRIMARY KEY,
    child_id INTEGER NOT NULL,

    program_name TEXT NOT NULL,

    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,

    allowed_time INTEGER NOT NULL,
    time_span TEXT NOT NULL,
    usage_time FLOAT NOT NULL
)
"""
CREATE_CHILDREN_TABLE = """
CREATE TABLE IF NOT EXISTS children (
    child_id INTEGER PRIMARY KEY,
    parent_email TEXT,
    name TEXT NOT NULL,
    time_limit_id INTEGER REFERENCES time_limits(id)
)
"""
CREATE_TIME_LIMITS_TABLE = """
CREATE TABLE IF NOT EXISTS time_limits (
    id INTEGER PRIMARY KEY,
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,
    allowed_time INTEGER NOT NULL,
    time_span TEXT NOT NULL,
    usage_time FLOAT NOT NULL
)"""
CREATE_KNOWN_PROGRAMS_TABLE = """
CREATE TABLE IF NOT EXISTS known_programs (
    child_id INTEGER NOT NULL,
    program_name TEXT NOT NULL,
    usage_time FLOAT NOT NULL,
    last_updated INTEGER NOT NULL,
    )
"""
ADD_RESTRICTION = """
INSERT INTO restrictions (child_id, program_name, start_time, end_time, allowed_time, time_span, usage_time)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""
GET_RESTRICTIONS = """
SELECT * FROM restrictions WHERE child_id = ?
"""
GET_RESTRICTION = """
SELECT * FROM restrictions WHERE child_id = ? AND program_name = ?
"""
REMOVE_RESTRICTION = """
DELETE FROM restrictions WHERE child_id = ? AND program_name = ?
"""
REMOVE_ALL_RESTRICTIONS = """
DELETE FROM restrictions WHERE child_id = ?
"""
GET_CHILDREN = """
SELECT * FROM children WHERE parent_email = ?
"""
ADD_CHILD = """
INSERT INTO children (child_id, parent_email, name)
VALUES (?, ?, ?)
"""

class RestrictionsDBRepository(IRestrictionsDBRepository):
    """
    Implementation of the restrictions database repository with sqlite3.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_RESTRICTIONS_TABLE)
        self.cursor.execute(CREATE_CHILDREN_TABLE)
        self.cursor.execute(CREATE_TIME_LIMITS_TABLE)
        self.cursor.execute(CREATE_KNOWN_PROGRAMS_TABLE)
        self.connection.commit()

    def add_restriction(self, restriction):
        self.cursor.execute(ADD_RESTRICTION, (restriction.child_id, restriction.program_name, restriction.start_time, restriction.end_time, restriction.allowed_time, restriction.time_span, restriction.usage_time))
        self.connection.commit()

    def get_child_id(self, parent_email, child_name):
        self.cursor.execute("SELECT child_id FROM children WHERE parent_email = ? AND name = ?", (parent_email, child_name))
        child_id = self.cursor.fetchone()
        if child_id is None: # Child not found
            return None
        return child_id[0]
    
    def get_len_all_restrictions(self):
        self.cursor.execute("SELECT COUNT(*) FROM restrictions")
        return self.cursor.fetchone()[0]

    def get_restrictions(self, child_id):
        self.cursor.execute(GET_RESTRICTIONS, (child_id,))
        return self.cursor.fetchall()
    
    def get_restriction(self, child_id, program_name):
        self.cursor.execute(GET_RESTRICTION, (child_id, program_name))
        return self.cursor.fetchone()
    
    def remove_restriction(self, child_id, program_name):
        print(f"Removing restriction with child_id: {child_id} and program_name: {program_name}")
        self.cursor.execute(REMOVE_RESTRICTION, (child_id, program_name))
        self.connection.commit()

    def update_restriction(self, restriction):
        self.remove_restriction(restriction.child_id, restriction.program_name)
        self.add_restriction(restriction)

    def remove_all_restrictions(self, child_id):
        self.cursor.execute(REMOVE_ALL_RESTRICTIONS, (child_id,))
        self.connection.commit()

    def get_children(self, email):
        self.cursor.execute(GET_CHILDREN, (email,))
        return self.cursor.fetchall()
    
    def add_child(self, child_id, parent_email, name):
        self.cursor.execute(ADD_CHILD, (child_id, parent_email, name))
        self.connection.commit()
        return True
    
    def get_time_limit(self, parent_email, child_id):
        
        self.cursor.execute("SELECT time_limit_id FROM children WHERE parent_email = ? AND child_id = ?", (parent_email, child_id))
        time_limit_id = self.cursor.fetchone()
        if time_limit_id is None: # Child not found
            return None
        
        self.cursor.execute("SELECT * FROM time_limits WHERE id = ?", (time_limit_id[0],))
        time_limit = self.cursor.fetchone()
        return time_limit
    
    def add_known_program(self, child_id, program_name):
        self.cursor.execute("INSERT INTO known_programs (child_id, program_name, usage_time, last_updated) VALUES (?, ?, 0, 0)", (child_id, program_name))
        self.connection.commit()
        return True
    
    def get_known_programs(self, child_id):
        self.cursor.execute("SELECT * FROM known_programs WHERE child_id = ?", (child_id,))
        return self.cursor.fetchall()
    
    def get_known_program(self, child_id, program_name):
        self.cursor.execute("SELECT * FROM known_programs WHERE child_id = ? AND program_name = ?", (child_id, program_name))
        return self.cursor.fetchone()
    
    def get_child_id_by_name(self, email, name):
        self.cursor.execute("SELECT child_id FROM children WHERE parent_email = ? AND name = ?", (email, name))
        child_id = self.cursor.fetchone()
        if child_id is None:
            return None
        return child_id[0]
    
    def update_usage_time(self, child_id, program_name, usage_time):
        self.cursor.execute("UPDATE known_programs SET usage_time = ? WHERE child_id = ? AND program_name = ?", (usage_time, child_id, program_name))
        self.connection.commit()
        return True
    
    def get_usage_of_program(self, child_id, program_name):
        self.cursor.execute("SELECT usage_time FROM known_programs WHERE child_id = ? AND program_name = ?", (child_id, program_name))
        usage_time = self.cursor.fetchone()
        if usage_time is None:
            return None
        return usage_time[0]
    
    def get_last_updated(self, child_id, program_name):
        self.cursor.execute("SELECT last_updated FROM known_programs WHERE child_id = ? AND program_name = ?", (child_id, program_name))
        last_updated = self.cursor.fetchone()
        if last_updated is None:
            return None
        return last_updated[0]
    
    def update_last_updated(self, child_id, program_name, last_updated):
        self.cursor.execute("UPDATE known_programs SET last_updated = ? WHERE child_id = ? AND program_name = ?", (last_updated, child_id, program_name))
        self.connection.commit()
        return True