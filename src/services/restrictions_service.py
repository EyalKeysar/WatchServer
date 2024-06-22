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
        # make sure there is no other restriction with the same program name
        if self.restrictions_db_repository.get_restriction(child_id, program_name) is not None:
            return False

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
    
    def update_program_usage(self, mac_addr, program_name, start_time):
        """
            Updates the usage time of a program.
        """
        start_time = int(start_time)
        current_time = int(datetime.now().timestamp())
        usage_time = current_time - start_time
        child_id = self.users_db_repository.get_child_id_by_mac(mac_addr)
        if child_id is None:
            return False
        
        last_update = self.restrictions_db_repository.get_last_updated(child_id, program_name)
        last_usage = self.restrictions_db_repository.get_usage_of_program(child_id, program_name)

        if last_update is "0":
            self.restrictions_db_repository.add_known_program(child_id, program_name)
            new_usage_time = usage_time
        else:
            # Assuming a threshold to determine if it's a new session or continuation
            # For example, if the program hasn't been updated in the last 10 minutes (600 seconds), consider it a new session
            threshold = 600
            if current_time - last_update > threshold:
                new_usage_time = last_usage + usage_time
            else:
                # If within threshold, consider it a continuation and only add the difference since the last update
                new_usage_time = last_usage + (current_time - last_update)

        # Update the usage time in the database
        self.restrictions_db_repository.update_usage_time(child_id, program_name, new_usage_time)

        # Update the last updated timestamp for the program
        self.restrictions_db_repository.update_last_updated(child_id, program_name, current_time)
        return True


        