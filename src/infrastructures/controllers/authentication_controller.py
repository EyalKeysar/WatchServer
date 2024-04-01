from infrastructures.controllers.i_controller import IController

class AuthenticationController(IController):
    """
    TODO: Add description
    """
    def __init__(self, authentication_service):
        self.authentication_service = authentication_service
        
    def run(self):
        raise NotImplementedError
        pass