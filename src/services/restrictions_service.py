from services.i_service import IService

from entities.restrictions_db_interface import IRestrictionsDBRepository
from ServerAPI.shared.SharedDTO import *
"""
    This class is responsible for handling the restrictions of the application.
"""
class RestrictionsService(IService):
    def __init__(self, users_db_repository: IRestrictionsDBRepository, restrictions_db_repository: IRestrictionsDBRepository):
        self.restrictions_db_repository = restrictions_db_repository
        self.users_db_repository = users_db_repository
    
    def add_restriction(self, email, child_name, program_name, start_time, end_time, allowed_time, time_span):
        """
            Adds a restriction to the database.
        """
        child_id = self.restrictions_db_repository.get_child_id(email, child_name)
        restriction_id = self.restrictions_db_repository.get_len_all_restrictions() + 1
        restriction = Restriction(restriction_id, child_id, program_name, start_time, end_time, allowed_time, time_span, 0)
        return self.restrictions_db_repository.add_restriction(restriction)
    

    def remove_restriction(self, email, child_name, program_name):
        """
            Removes a restriction from the database.
        """
        child_id = self.restrictions_db_repository.get_child_id(email, child_name)
        return self.restrictions_db_repository.remove_restriction(child_id, program_name)
    
    def add_known_program(self, mac_addr, programs_list):
        """
            Updates the known programs of the child.
        """
        print("add known program ", mac_addr, programs_list)
        child_id = self.users_db_repository.get_child_id_by_mac(mac_addr)
        if child_id is None:
            return False
        programs_list = StringListSerializer.deserialize(programs_list)
        for program_name in programs_list:
            if self.restrictions_db_repository.get_known_program(child_id, program_name) is not None:
                continue
            else:
                self.restrictions_db_repository.add_known_program(child_id, program_name)
        return True
        