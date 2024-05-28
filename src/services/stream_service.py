from services.i_service import IService

from entities.restrictions_db_interface import IRestrictionsDBRepository
from ServerAPI.shared.SharedDTO import *

MAX_FRAMES_QUEUE_SIZE = 10
"""
    This class is responsible for handling the sreaming services of the application.
"""
class StreamService(IService):
    def __init__(self, users_db_repository: IRestrictionsDBRepository, restrictions_db_repository: IRestrictionsDBRepository):
        self.restrictions_db_repository = restrictions_db_repository
        self.users_db_repository = users_db_repository
        self.streams = {}  # {(mac_addr, type, email): frames_queue}

    def subscribe(self, email, child_name, type):
        child_id = self.restrictions_db_repository.get_child_id_by_name(email, child_name)
        mac_addr = self.users_db_repository.get_mac_addr(email, child_id)

        if (mac_addr, type, email) not in self.streams:
            print(f"{email} Subscribing to {mac_addr}-{type}")
            self.streams[(mac_addr, type, email)] = []
        return True

    def unsubscribe(self, email, child_name, type):
        child_id = self.restrictions_db_repository.get_child_id_by_name(email, child_name)
        mac_addr = self.users_db_repository.get_mac_addr(email, child_id)

        if (mac_addr, type, email) in self.streams:
            print(f"{email} Unsubscribing from {mac_addr}-{type}")
            del self.streams[(mac_addr, type, email)]
    
    def get_frame(self, email, child_name, type):
        child_id = self.restrictions_db_repository.get_child_id_by_name(email, child_name)
        mac_addr = self.users_db_repository.get_mac_addr(email, child_id)

        frame = None
        if (mac_addr, type, email) in self.streams and len(self.streams[(mac_addr, type, email)]) > 0:
            frame = self.streams[(mac_addr, type, email)].pop(0)
        

        if len(self.streams[(mac_addr, type, email)]) > MAX_FRAMES_QUEUE_SIZE:
            self.streams[(mac_addr, type, email)].pop(0)

        return frame
    
    def set_frame(self, mac_addr, type, frame):
        print(f"Setting frame to {mac_addr}-{type}")
        for key in self.streams:
            if key[0] == mac_addr and key[1] == type:
                self.streams[key].append(frame)
                print(f"Frame added to {mac_addr}-{type}")
                if len(self.streams[key]) > MAX_FRAMES_QUEUE_SIZE:
                    self.streams[key].pop(0)

        return True