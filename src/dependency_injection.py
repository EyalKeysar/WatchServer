from infrastructures.users_db_repo import UsersDBRepository
from infrastructures.restrictions_db_repo import RestrictionsDBRepository

from services.authentication_service import AuthenticationService
from services.children_manager_service import ChildrenManagerService
from services.fetch_service import FetchService
from services.restrictions_service import RestrictionsService
from services.stream_service import StreamService

from infrastructures.controllers.authentication_controller import AuthenticationController
from infrastructures.controllers.children_manager_controller import ChildrenManagerController
from infrastructures.controllers.fetch_controller import FetchController
from infrastructures.controllers.restrictions_controller import RestrictionsController
from infrastructures.controllers.stream_controller import StreamController

from controllers_container import ControllersContainer

USERS_DB_PATH = "data/users.db"
RESTRICTIONS_DB_PATH = "data/restrictions.db"


def inject():
    users_db_repo = UsersDBRepository(USERS_DB_PATH)
    restrictions_db_repo = RestrictionsDBRepository(RESTRICTIONS_DB_PATH)

    auth_s = AuthenticationService(users_db_repo, restrictions_db_repo)
    children_manager_s = ChildrenManagerService(users_db_repo,
                                                restrictions_db_repo)
    fetch_s = FetchService(users_db_repo, restrictions_db_repo)
    restrictions_s = RestrictionsService(users_db_repo, restrictions_db_repo)
    stream_s = StreamService(users_db_repo, restrictions_db_repo)


    auth_c = AuthenticationController(auth_s)
    children_manager_c = ChildrenManagerController(children_manager_s)
    fetch_c = FetchController(fetch_s)
    restrictions_c = RestrictionsController(restrictions_s)
    stream_c = StreamController(stream_s)

    controlers_container = ControllersContainer(auth_c,
                                                children_manager_c,
                                                restrictions_c,
                                                fetch_c,
                                                stream_c)

    return controlers_container
