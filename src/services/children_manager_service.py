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

    def confirm_agent(self, parent_email, auth_string, child_name):
        is_valid = self.users_db_repo.validate_auth_str(auth_string)
        if not is_valid:
            return "Invalid auth string"
        mac_address = self.users_db_repo.get_waiting_agent_mac_address(auth_string)
        if mac_address is None:
            return "smthing went wrong with the mac address of waiting agent or the auth string"

        # variables i have at this point: parent_email, auth_string, child_name, mac_address

        self.users_db_repo.remove_waiting_agent(auth_string)

        child_id = self.users_db_repo.add_child(mac_address, parent_email, auth_string)

        self.restrictions_db_repo.add_child(child_id, parent_email, child_name)

        return "Agent confirmed successfully"


        
        
        # child_id = self.get_child_id()
        # self.restrictions_db_repo.add_child(child_id, parent_email, "name")
        # return "Agent confirmed successfully"