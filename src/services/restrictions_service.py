from services.i_service import IService

from entities.restrictions_db_interface import IRestrictionsDBRepository

"""
    This class is responsible for handling the restrictions of the application.
"""
class RestrictionsService(IService):
    def __init__(self, restrictions_db_repository: IRestrictionsDBRepository):
        self.restrictions_db_repository = restrictions_db_repository
    
    def add_restriction():
        pass

    def remove_restriction():
        pass