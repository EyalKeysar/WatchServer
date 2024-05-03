from services.i_service import IService

from entities.restrictions_db_interface import IRestrictionsDBRepository
from ServerAPI.shared.SharedDTO import *
"""
    This class is responsible for handling the restrictions of the application.
"""
class RestrictionsService(IService):
    def __init__(self, restrictions_db_repository: IRestrictionsDBRepository):
        self.restrictions_db_repository = restrictions_db_repository
    
    def add_restriction(self, email, child_name, program_name, start_time, end_time, allowed_time, time_span):
        """
            Adds a restriction to the database.
        """
        child_id = self.restrictions_db_repository.get_child_id(email, child_name)
        restriction_id = self.restrictions_db_repository.get_len_all_restrictions() + 1
        restriction = Restriction(restriction_id, child_id, program_name, start_time, end_time, allowed_time, time_span, 0)
        return self.restrictions_db_repository.add_restriction(restriction)
        