from hashlib import sha256
import time
from datetime import datetime
from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository
from entities.restrictions_db_interface import IRestrictionsDBRepository
from ServerAPI.shared.SharedDTO import ParentData

class AuthenticationService(IService):
    def __init__(self, users_db_repository: IUsersDBRepository, restrictions_db_repository: IRestrictionsDBRepository):
        self.users_db_repository = users_db_repository

    def signup(self, email, password, username):
        
        if email is None or password is None or username is None:
            print("Invalid input")
            return False, None
        elif len(username) < 4 or len(password) < 4:
            print("Username and password must be at least 4 characters long")
            return False, None
        elif '@' not in email or '.' not in email or email.count('@') > 1 or email.count('.') > 1 or email.index('@') > email.index('.') or len(email) < 6:
            print("Invalid email")
            return False, None
        

        parent = ParentData(email, username, sha256(password.encode()).hexdigest())
        if self.users_db_repository.add_parent(parent):
            print("Parent added successfully")
            return True, parent.email
        print("Parent already exists")
        return False, None
        

    def login(self, email, password):
        respond, name, password_hash = self.users_db_repository.get_parent(email)
        if not respond:
            print("Parent not found")
            return False, None
        elif password is None or len(password) < 4:
            return False, None
        
        parent = ParentData(email, name, password_hash)
        if parent is None:
            print("Parent not found")
            return False, None
        if parent.password_hash == sha256(password.encode()).hexdigest():
            print("Parent logged in successfully")
            return True, parent.email
        print("Incorrect password")
        return False, None
    
    def new_agent(self, mac_address):
        current_time = datetime.now()
        auth_string = sha256(f"{mac_address}{current_time}".encode()).hexdigest()[:6]
        self.users_db_repository.new_agent(mac_address, current_time, auth_string)
        return auth_string, None

    def login_agent(self, auth_str):
        respond, mac_address = self.users_db_repository.get_agent(auth_str)
        if not respond:
            print("Agent not found")
            return False, None
        print("Agent logged in successfully")
        return True, mac_address