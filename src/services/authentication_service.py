from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository
from entities.dto.DTO import Parent
class AuthenticationService(IService):
    def __init__(self, users_db_repository: IUsersDBRepository):
        self.users_db_repository = users_db_repository

    def signup(self, email, username, password):
        parent = Parent(email, username, password)
        self.users_db_repository.add_parent(parent)
        return "Parent added successfully"

    def login(self, username, password):
        parent = self.users_db_repository.get_parent(username)
        
        
