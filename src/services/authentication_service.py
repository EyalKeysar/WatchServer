from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository

class AuthenticationService(IService):
    def __init__(self, users_db_repository: IUsersDBRepository):
        self.users_db_repository = users_db_repository

    def login():
        pass

    def signup():
        pass