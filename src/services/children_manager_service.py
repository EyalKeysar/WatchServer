from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository
from entities.restrictions_db_interface import IRestrictionsDBRepository

from ServerAPI.shared.SharedDTO import *

import datetime

class ChildrenManagerService(IService):
    def __init__(self, users_db_repo: IUsersDBRepository, restrictions_db_repo: IRestrictionsDBRepository):
        self.users_db_repo = users_db_repo
        self.restrictions_db_repo = restrictions_db_repo

    def confirm_agent(self, parent_email, auth_string, child_name):
        time_stamp = self.users_db_repo.get_time_stamp(auth_string)
        if time_stamp is None:
            return "Invalid auth string"
        time = datetime.datetime.now()
        agent_time = datetime.datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S.%f")
        if (time - agent_time).seconds > 300: # 5 minutes
            return "Auth string expired"
        
        mac_address = self.users_db_repo.get_waiting_agent_mac_address(auth_string)
        if mac_address is None:
            return "Invalid auth string"
        
        self.users_db_repo.remove_waiting_agent(auth_string)

        children = self.users_db_repo.get_all_children()
        child_id = len(children) + 1

        response = self.users_db_repo.add_child(mac_address, parent_email, auth_string, child_id)
        if not response:
            return "Error adding child to database"
        response = self.restrictions_db_repo.add_child(child_id, parent_email, child_name)
        if not response:
            return "Error adding child to 2nd database"
        return "Agent confirmed successfully"