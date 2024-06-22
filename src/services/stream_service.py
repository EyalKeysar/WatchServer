from services.i_service import IService

from entities.restrictions_db_interface import IRestrictionsDBRepository
from ServerAPI.shared.SharedDTO import *
import os
import pickle
from PIL import Image
import base64
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
            self.streams[(mac_addr, type, email)] = None
        return True

    def unsubscribe(self, email, child_name, type):
        child_id = self.restrictions_db_repository.get_child_id_by_name(email, child_name)
        mac_addr = self.users_db_repository.get_mac_addr(email, child_id)

        if (mac_addr, type, email) in self.streams:
            print(f"{email} Unsubscribing from {mac_addr}-{type}")
            del self.streams[(mac_addr, type, email)]
        return True
    
    def get_frame(self, email, child_name, stream_type):
        child_id = self.restrictions_db_repository.get_child_id_by_name(email, child_name)
        mac_addr = self.users_db_repository.get_mac_addr(email, child_id)

        if (mac_addr, stream_type, email) in self.streams:
            if self.streams[(mac_addr, stream_type, email)] is None:
                return None
            frame = self.streams[(mac_addr, stream_type, email)]
            return frame
        return None
    
    
    def set_frame(self, mac_addr, type, frame):
        for key in self.streams:
            if key[0] == mac_addr and key[1] == type:
                self.streams[key] = frame

        return True