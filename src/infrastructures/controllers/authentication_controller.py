from infrastructures.controllers.i_controller import IController

class AuthenticationController(IController):
    """
    TODO: Add description
    """
    def __init__(self, authentication_service):
        self.authentication_service = authentication_service
        
    def run(self, *args):
        if args[0] == "login":
            return self.authentication_service.login(args[1], args[2])
        elif args[0] == "signup":
            return self.authentication_service.signup(args[1], args[2], args[3])