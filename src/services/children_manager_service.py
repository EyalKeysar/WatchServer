from typing import Any
from services.i_service import IService

from entities.users_db_interface import IUsersDBRepository
from entities.restrictions_db_interface import IRestrictionsDBRepository
class ChildrenManagerService(IService):
    def __init__(self, users_db_repo: IUsersDBRepository, restrictions_db_repo: IRestrictionsDBRepository):
        self.users_db_repo = users_db_repo
        self.restrictions_db_repo = restrictions_db_repo

    def add_child():
        pass
    
    def remove_child():
        pass