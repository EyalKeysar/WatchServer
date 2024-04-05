from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository
from entities.restrictions_db_interface import IRestrictionsDBRepository

from entities.dto.DTO import Parent
class FetchService(IService):
    """
    Service for fetching data from the database.
    """

    def __init__(self, users_db_repo: IUsersDBRepository, restrictions_db_repo: IRestrictionsDBRepository):
        self.users_db_repo = users_db_repo
        self.restrictions_db_repo = restrictions_db_repo
        
    def handle(self, request):
        """
        Handles the request.
        """
        command, request = request.split("|")
        return self.fetch(command, request)
    
    def fetch(self, command, request):
        """
        Fetches data from the database.
        """
        command_to_function = {
            "parents": self.fetch_parents,
            "children": self.fetch_children
        }
        return command_to_function[command]()

    
    def fetch_parents(self):
        """
        Fetches parents from the database.
        """
        return self.users_db_repo.get_parents()
    
    def fetch_children(self):
        """
        Fetches children from the database.
        """
        return self.users_db_repo.get_children()