import json
from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository
from entities.restrictions_db_interface import IRestrictionsDBRepository

from ServerAPI.shared.SharedDTO import *
class FetchService(IService):
    """
    Service for fetching data from the database.
    """

    def __init__(self, users_db_repo: IUsersDBRepository, restrictions_db_repo: IRestrictionsDBRepository):
        self.users_db_repo = users_db_repo
        self.restrictions_db_repo = restrictions_db_repo
    
    def fetch_children(self, email):
        """
        Fetches children from the database.
        """
        children_raw = self.restrictions_db_repo.get_children(email)

        children = []
        for child in children_raw:
            child_id = child[0]
            parent_email = child[1]
            child_name = child[2]
            restrictions = []
            time_limit = self.restrictions_db_repo.get_time_limit(email, child_id)
            for restriction in self.restrictions_db_repo.get_restrictions(child_id):
                restrictions.append(Restriction(restriction[0], restriction[1], restriction[2], restriction[3], restriction[4], restriction[5]))

            children.append(ChildData(child_id, parent_email, child_name, restrictions, time_limit))
            print("children = ", ChildData(child_id, parent_email, child_name, restrictions, time_limit).child_id)

        return ChildListSerializer.serialize(children)
        
        # return self.users_db_repo.get_children()

    def fetch_restrictions(self, email, child_name):
        """
        Fetches restrictions for a child.
        """
        child_id = self.restrictions_db_repo.get_child_id(email, child_name)
        restrictions_raw = self.restrictions_db_repo.get_restrictions(child_id)
        restrictions_list = []
        for restriction in restrictions_raw:
            restrictions_list.append(RestrictionSerializer.serialize(Restriction(restriction[0], restriction[1], restriction[2], restriction[3], restriction[4], restriction[5], restriction[6], restriction[7])))

        return json.dumps(restrictions_list)


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