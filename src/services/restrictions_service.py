from services.i_service import IService

from entities.restrictions_db_interface import IRestrictionsDBRepository
from ServerAPI.shared.SharedDTO import *

from datetime import datetime
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
    
    def update_known_programs(self, mac_addr, programs_list):
        """
            Updates the known programs of the child.
        """
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
    
    def update_program_usage(self, mac_addr, program_name, start_time, usage_time):
        """
            Updates the usage time of a program.
        """
        child_id = self.users_db_repository.get_child_id_by_mac(mac_addr)
        if child_id is None:
            return False
        

        last_update = self.restrictions_db_repository.get_last_updated(child_id, program_name)
        last_usage = self.restrictions_db_repository.get_usage_of_program(child_id, program_name)

        if last_update is None:
            self.restrictions_db_repository.add_known_program(child_id, program_name)
            last_update = 0

        # get curernt time as int
        current_time = int(datetime.now().timestamp())

        if str(last_update) == "0":
            self.restrictions_db_repository.update_usage_time(child_id, program_name, usage_time)
        else:
            if start_time - last_update > 0:
                self.restrictions_db_repository.update_usage_time(child_id, program_name, usage_time + last_usage)
            else:
                delta_time = current_time - start_time
                self.restrictions_db_repository.update_usage_time(child_id, program_name, delta_time + last_usage)
        self.restrictions_db_repository.update_last_updated(child_id, program_name, current_time)


        