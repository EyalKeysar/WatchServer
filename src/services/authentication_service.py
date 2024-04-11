from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository
from entities.dto.DTO import Parent
class AuthenticationService(IService):
    def __init__(self, users_db_repository: IUsersDBRepository):
        self.users_db_repository = users_db_repository

    def signup(self, email, password, username):
        parent = Parent(email, username, password)
        if self.users_db_repository.add_parent(parent):
            print("Parent added successfully")
            return True
        print("Parent already exists")
        return False
        

    def login(self, email, password):
        parent = self.users_db_repository.get_parent(email)
        
        
