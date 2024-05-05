from infrastructures.controllers.i_controller import IController

class AuthenticationController(IController):
    """
    Controller for authentication operations.
    """
    def __init__(self, authentication_service):
        self.authentication_service = authentication_service
        self.commands = {
            "login": [self.authentication_service.login, ["email", "password"]],
            "signup": [self.authentication_service.signup, ["email", "password", "username"]],
            "new_agent": [self.authentication_service.new_agent, ["mac_address"]],
            "login_agent": [self.authentication_service.login_agent, ["auth_str"]]
        }
        
    def run(self, *args):
        command = args[0]
        if command not in self.commands:
            return "Command not found"
        
        if(len(args) != len(self.commands[command][1]) + 1): # +1 for the command itself
            return "Invalid number of arguments"
        
        return self.commands[command][0](*args[1:])
        