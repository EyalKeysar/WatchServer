from infrastructures.controllers.i_controller import IController

class FetchController(IController):
    """
    TODO: Add description
    """
    def __init__(self, fetch_service):
        self.fetch_service = fetch_service
        
    def run(self, *args):
        if args[0] == "parents":
            return self.fetch_service.fetch_parents()
        elif args[0] == "info":
            print("fetching info")
            return self.fetch_service.fetch_info()
        elif args[0] == "children":
            return self.fetch_service.fetch_children()
        else:
            print("Invalid command!, args: ", args)
        