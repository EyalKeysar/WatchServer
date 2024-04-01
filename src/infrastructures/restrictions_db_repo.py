from entities.restrictions_db_interface import IRestrictionsDBRepository

import sqlite3

class RestrictionsDBRepository(IRestrictionsDBRepository):
    """
    Implementation of the restrictions database repository with sqlite3.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS restrictions (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT
            )
            """
        )
        self.connection.commit()

    def add_restriction(self, restriction):
        self.cursor.execute(
            """
            INSERT INTO restrictions (name, description) VALUES (?, ?)
            """, (restriction.name, restriction.description)
        )
        self.connection.commit()

    def remove_restriction(self, restriction):
        self.cursor.execute(
            """
            DELETE FROM restrictions WHERE id = ?
            """, (restriction.id,)
        )
        self.connection.commit()

    def get_restrictions(self):
        self.cursor.execute(
            """
            SELECT id, name, description FROM restrictions
            """
        )
        return self.cursor.fetchall()
    
    def get_restriction(self, restriction):
        self.cursor.execute(
            """
            SELECT id, name, description FROM restrictions WHERE id = ?
            """, (restriction.id,)
        )
        return self.cursor.fetchone()
    
    def update_restriction(self, restriction):
        self.cursor.execute(
            """
            UPDATE restrictions SET name = ?, description = ? WHERE id = ?
            """, (restriction.name, restriction.description, restriction.id)
        )
        self.connection.commit()