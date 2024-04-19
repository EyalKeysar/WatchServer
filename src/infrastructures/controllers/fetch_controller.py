from infrastructures.controllers.i_controller import IController

class FetchController(IController):
    """
    Controller for fetching data from databases.
    """
    def __init__(self, fetch_service):
        self.fetch_service = fetch_service

        self.commands = {
            "parents": [self.fetch_service.fetch_parents, []],
            "info": [self.fetch_service.fetch_info, []],
            "children": [self.fetch_service.fetch_children, []]
        }
        
    def run(self, *args):
        command = args[0]
        if command not in self.commands:
            return "Command not found"
        
        if(len(args) != len(self.commands[command][1]) + 1):
            return "Invalid number of arguments"
        
        return self.commands[command][0](*args[1:])