from entities.users_db_interface import IUsersDBRepository
from entities.restrictions_db_interface import IRestrictionsDBRepository

from infrastructures.users_db_repo import UsersDBRepository
from infrastructures.restrictions_db_repo import RestrictionsDBRepository

from services.authentication_service import AuthenticationService
from services.children_manager_service import ChildrenManagerService
from services.fetch_service import FetchService
from services.restrictions_service import RestrictionsService

from infrastructures.controllers.authentication_controller import AuthenticationController
from infrastructures.controllers.children_manager_controller import ChildrenManagerController
from infrastructures.controllers.fetch_controller import FetchController
from infrastructures.controllers.restrictions_controller import RestrictionsController

from controllers_container import ControllersContainer

USERS_DB_PATH = "data/users.db"
RESTRICTIONS_DB_PATH = "data/restrictions.db"

def inject():
    
    users_db_repo = UsersDBRepository(USERS_DB_PATH)
    restrictions_db_repo = RestrictionsDBRepository(RESTRICTIONS_DB_PATH)

    auth_s = AuthenticationService(users_db_repo)
    children_manager_s = ChildrenManagerService(users_db_repo, restrictions_db_repo)
    fetch_s = FetchService(users_db_repo, restrictions_db_repo)
    restrictions_s = RestrictionsService(restrictions_db_repo)
    
    auth_c = AuthenticationController(auth_s)
    children_manager_c = ChildrenManagerController(children_manager_s)
    fetch_c = FetchController(fetch_s)
    restrictions_c = RestrictionsController(restrictions_s)
    
    controlers_container = ControllersContainer(auth_c, children_manager_c, restrictions_c, fetch_c)

    return controlers_container