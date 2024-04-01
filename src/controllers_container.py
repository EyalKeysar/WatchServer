from infrastructures.controllers.authentication_controller import AuthenticationController
from infrastructures.controllers.children_manager_controller import ChildrenManagerController
from infrastructures.controllers.restrictions_controller import RestrictionsController
from infrastructures.controllers.fetch_controller import FetchController

class ControllersContainer:
    def __init__(self, 
                 authentication_controller: AuthenticationController, 
                 children_manager_controller: ChildrenManagerController, 
                 restrictions_controller: RestrictionsController, 
                 fetch_controller: FetchController
                 ):
        self.authentication_controller = authentication_controller
        self.children_manager_controller = children_manager_controller
        self.restrictions_controller = restrictions_controller
        self.fetch_controller = fetch_controller
        