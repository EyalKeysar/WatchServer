from infrastructures.controllers.i_controller import IController

class ChildrenManagerController(IController):
    """
    TODO: Add description
    """
    def __init__(self, children_manager_service):
        self.children_manager_service = children_manager_service
        
    def run(self, *args):
        if args[0] == "add":
            return self.children_manager_service.add_child(args[1])
        elif args[0] == "remove":
            return self.children_manager_service.remove_child(args[1])
        
        # !! UPDATE CHILD !!