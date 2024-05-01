from infrastructures.controllers.i_controller import IController

class ChildrenManagerController(IController):
    """
    TODO: Add description
    """
    def __init__(self, children_manager_service):
        self.children_manager_service = children_manager_service

        self.commands = {
            "confirm_agent": [self.children_manager_service.confirm_agent, ["auth_string", "child_name"]]
        }
        # !! UPDATE CHILD !!
        
    def run(self, *args):
        email = args[0]
        command = args[1]
        args = args[2:]
        if command not in self.commands:
            return "Command not found"
        
        if(len(args) != len(self.commands[command][1])):
            return "Invalid number of arguments"
        
        # test print args
        print(f"args: {args}")
        
        return self.commands[command][0](email, *args)