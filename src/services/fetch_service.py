from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository
from entities.restrictions_db_interface import IRestrictionsDBRepository

from ServerAPI.shared.SharedDTO import ParentData
class FetchService(IService):
    """
    Service for fetching data from the database.
    """

    def __init__(self, users_db_repo: IUsersDBRepository, restrictions_db_repo: IRestrictionsDBRepository):
        self.users_db_repo = users_db_repo
        self.restrictions_db_repo = restrictions_db_repo
    
    def fetch_parents(self):
        """
        Fetches parents from the database.
        """
        return self.users_db_repo.get_parents()
    
    def fetch_children(self, email):
        """
        Fetches children from the database.
        """
        raise NotImplementedError
        # return self.users_db_repo.get_children()
    
    def fetch_info(self):
        """
        Fetches information about the user.
        """
        return "Hello from FetchService!"
    
    def fetch_statistics(self, child_id):
        """
        Fetches statistics for a child.
        """
        return self.users_db_repo.get_statistics(child_id)