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
        return self.fetch(request)
        pass
    
    def fetch(self, request):
        """
        Fetches data from the database.
        """
        n_parent = Parent("asd@gmail.com", "av")
        self.users_db_repo.add_parent(n_parent)
        self.users_db_repo.get_parents()