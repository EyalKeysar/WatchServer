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