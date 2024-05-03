from infrastructures.controllers.i_controller import IController

class RestrictionsController(IController):
    """
    TODO: Add description
    """
    def __init__(self, restrictions_service):
        self.restrictions_service = restrictions_service

        self.commands = {
            "add_restriction": (self.restrictions_service.add_restriction, ["child_name", "program_name", "start_time", "end_time", "allowed_time", "time_span"])
        }

    def run(self, *args):
        email = args[0]
        command = args[1]
        args = args[2:]
        if command not in self.commands:
            return "Command not found"

        if(len(args) != len(self.commands[command][1])):
            return "Invalid number of arguments"

        return self.commands[command][0](email, *args)