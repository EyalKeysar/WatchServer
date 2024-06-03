from infrastructures.controllers.i_controller import IController

class StreamController(IController):
    """
    TODO: Add description
    """
    def __init__(self, stream_service):
        self.stream_service = stream_service

        self.commands = {
            "subscribe": [self.stream_service.subscribe, ["child_name", "type"]],
            "unsubscribe": [self.stream_service.unsubscribe, ["child_name", "type"]],
            "get_frame": [self.stream_service.get_frame, ["child_name", "type"]],
            "set_frame": [self.stream_service.set_frame, ["type", "frame"]],

        }

    def run(self, *args):
        email = args[0]
        command = args[1]
        args = args[2:]
        if command not in self.commands:
            print(f"Command not found: {command}")
            return "Command not found"

        if(len(args) != len(self.commands[command][1])):
            print(f"Invalid number of arguments: {len(args)} != {len(self.commands[command][1])}")
            return "Invalid number of arguments"

        return self.commands[command][0](email, *args)