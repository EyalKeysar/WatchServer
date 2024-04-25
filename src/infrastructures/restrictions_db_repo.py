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

class RestrictionsDBRepository(IRestrictionsDBRepository):
    """
    Implementation of the restrictions database repository with sqlite3.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_RESTRICTIONS_TABLE)
        self.connection.commit()

    def add_restriction(self, restriction):
        self.cursor.execute(ADD_RESTRICTION, (restriction.child_id, restriction.program_name, restriction.start_time, restriction.end_time, restriction.allowed_time, restriction.time_span, restriction.usage_time))
        self.connection.commit()

    def get_restrictions(self, child_id):
        self.cursor.execute(GET_RESTRICTIONS, (child_id,))
        return self.cursor.fetchall()
    
    def get_restriction(self, child_id, program_name):
        self.cursor.execute(GET_RESTRICTION, (child_id, program_name))
        return self.cursor.fetchone()
    
    def remove_restriction(self, child_id, program_name):
        self.cursor.execute(REMOVE_RESTRICTION, (child_id, program_name))
        self.connection.commit()

    def update_restriction(self, restriction):
        self.remove_restriction(restriction.child_id, restriction.program_name)
        self.add_restriction(restriction)

    def remove_all_restrictions(self, child_id):
        self.cursor.execute(REMOVE_ALL_RESTRICTIONS, (child_id,))
        self.connection.commit()