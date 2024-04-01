from infrastructures.controllers.i_controller import IController

class RestrictionsController(IController):
    """
    TODO: Add description
    """
    def __init__(self, restrictions_service):
        self.restrictions_service = restrictions_service

    def run(self):
        raise NotImplementedError
        pass