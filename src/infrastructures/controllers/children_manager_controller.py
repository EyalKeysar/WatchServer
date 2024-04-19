from infrastructures.controllers.i_controller import IController

class ChildrenManagerController(IController):
    """
    TODO: Add description
    """
    def __init__(self, children_manager_service):
        self.children_manager_service = children_manager_service

        self.commands = {
            "add": [self.children_manager_service.add_child, ["name"]],
            "remove": [self.children_manager_service.remove_child, ["name"]]
        }
        # !! UPDATE CHILD !!
        
    def run(self, *args):
        command = args[0]
        if command not in self.commands:
            return "Command not found"
        
        if(len(args) != len(self.commands[command][1]) + 1): # +1 for the command itself
            return "Invalid number of arguments"
        
        return self.commands[command][0](*args[1:])