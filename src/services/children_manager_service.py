from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository
from entities.restrictions_db_interface import IRestrictionsDBRepository

from ServerAPI.shared.SharedDTO import *

class ChildrenManagerService(IService):
    def __init__(self, users_db_repo: IUsersDBRepository, restrictions_db_repo: IRestrictionsDBRepository):
        self.users_db_repo = users_db_repo
        self.restrictions_db_repo = restrictions_db_repo

    def add_child(self, child):
        self.restrictions_db_repo
        # .add_child(child)
        return "Child added successfully"
    
    def remove_child():
        pass

    def confirm_agent(self, parent_email, auth_string):
        self.users_db_repo.confirm_agent(parent_email, auth_string)
        child_id = self.get_child_id()
        self.restrictions_db_repo.add_child(child_id, parent_email, "name")
        return "Agent confirmed successfully"