from infrastructures.controllers.i_controller import IController

class ChildrenManagerController(IController):
    """
    TODO: Add description
    """
    def __init__(self, children_manager_service):
        self.children_manager_service = children_manager_service
        
    def run(self):
        raise NotImplementedError
        pass