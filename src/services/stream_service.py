from services.i_service import IService

from entities.restrictions_db_interface import IRestrictionsDBRepository
from ServerAPI.shared.SharedDTO import *
import os
import pickle
from PIL import Image
import base64
MAX_FRAMES_QUEUE_SIZE = 2
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
    
    def get_frame(self, email, child_name, stream_type):
        child_id = self.restrictions_db_repository.get_child_id_by_name(email, child_name)
        mac_addr = self.users_db_repository.get_mac_addr(email, child_id)

        frame_path = f"frames/18-screen.png"
        if not os.path.exists(frame_path):
            print(f"Frame file not found: {frame_path}")
            return "Frame not found"

        frame = Image.open(frame_path)
        frame_bytes = pickle.dumps(frame)
        frame_base64 = base64.b64encode(frame_bytes).decode('utf-8')

        print(f"Sending frame of type: {type(frame)}, size: {len(frame_base64)}")

        return frame_base64
    
    def set_frame(self, mac_addr, type, frame):
        frame_bytes = base64.b64decode(frame)
        frame_bytes = pickle.loads(frame_bytes)
        # save frame to file
        if not os.path.exists('frames'):
            os.makedirs('frames')
        frame_bytes.save(f"frames/{mac_addr[:2]}-{type}.png")

        print(f"Setting frame to {mac_addr}-{type}")
        for key in self.streams:
            if key[0] == mac_addr and key[1] == type:
                self.streams[key].append(frame)
                print(f"Frame added to {mac_addr}-{type}")
                if len(self.streams[key]) > MAX_FRAMES_QUEUE_SIZE:
                    self.streams[key].pop(0)

        return True