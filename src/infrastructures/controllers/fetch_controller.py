from infrastructures.controllers.i_controller import IController

class FetchController(IController):
    """
    TODO: Add description
    """
    def __init__(self, fetch_service):
        self.fetch_service = fetch_service
        
    def run(self, request):
        return self.fetch_service.fetch(request)
        