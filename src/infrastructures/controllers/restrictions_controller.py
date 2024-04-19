from infrastructures.controllers.i_controller import IController

class RestrictionsController(IController):
    """
    TODO: Add description
    """
    def __init__(self, restrictions_service):
        self.restrictions_service = restrictions_service

        self.commands = {
        }

    def run(self, *args):
        command = args[0]
        if command not in self.commands:
            return "Command not found"
        
        if(len(args) != len(self.commands[command][1]) + 1):
            return "Invalid number of arguments"
        
        return self.commands[command][0](*args[1:])