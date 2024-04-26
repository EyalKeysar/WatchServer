from infrastructures.controllers.authentication_controller import AuthenticationController
from infrastructures.controllers.children_manager_controller import ChildrenManagerController
from infrastructures.controllers.restrictions_controller import RestrictionsController
from infrastructures.controllers.fetch_controller import FetchController

class ControllersContainer:
    def __init__(self, 
                 authentication_controller: AuthenticationController, 
                 children_manager_controller: ChildrenManagerController, 
                 restrictions_controller: RestrictionsController, 
                 fetch_controller: FetchController
                 ):
        self.authentication_controller = authentication_controller
        self.children_manager_controller = children_manager_controller
        self.restrictions_controller = restrictions_controller
        self.fetch_controller = fetch_controller
        self.authenticated_connections = []

    def handle(self, connection_id, request): # in socket the connection_id is the socket object
        command_to_controller = {
            "auth": self.authentication_controller,
            "manage": self.children_manager_controller,
            "restrict": self.restrictions_controller,
            "fetch": self.fetch_controller
        }
        command, *args = request.split("|")

        if command not in command_to_controller:
            return "Command not found"
        
        if command != "auth" and connection_id not in self.authenticated_connections:
            return "Not authenticated"
        elif command == "auth":
            response, email = command_to_controller[command].run(*args)
            print(f"Authenticated: {response} | {email}")
            if response == True:
                self.authenticated_connections.append((connection_id, email))
            return response
        else:
            email = None
            for connection in self.authenticated_connections:
                if connection[0] == connection_id:
                    email = connection[1]
                    break

            args = [email] + args
            return command_to_controller[command].run(*args)
        