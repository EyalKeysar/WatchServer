import hashlib
class Parent:
    """
    Parent DTO
    """
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def get_password_hash(self):
        return hashlib.sha256(self.password.encode()).hexdigest()


class Child:
    """
    Child DTO
    """
    def __init__(self, id, name, parent_id):
        self.id = id
        self.name = name
        self.parent_id = parent_id

class Restriction:
    """
    Restriction DTO
    """
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description