from dataclasses import dataclass, field
from typing import ClassVar
from coolname import generate_slug
import websockets

@dataclass()
class Room:
    name: ClassVar[str]
    users: ClassVar[list]

    def __post_init__(self):
        self.name = generate_slug(2)
        self.users = []

    def __str__(self):
        return self.name
    
    def list_users(self):
        return ",\n".join(self.users)
    
    def sent_broadcast(self, message, users =  None):
        if users is None:
            users = self.users

        websockets.broadcast(users, message)
    
    def join_room(self, user_socket):
        self.users.append(user_socket)
        self.sent_broadcast(f"{user_socket.id} joined the room")

    def sent_private_message(self, private):
        user_id, message = private.split(" ", maxsplit=1)
        send_to = None

        for user in self.users:
            print(user, user.id, user_id, str(user_id) == str(user.id))
            if str(user_id) == str(user.id):
                send_to = user
        
        if send_to is None:
            raise ValueError("Invalid User")

        self.sent_broadcast(message, [send_to])
    
    def exit_room(self, user):
        self.users.remove(user)
        return True
        
    
@dataclass()
class RoomManager:
    rooms: dict = field(init=False, default_factory=dict)

    def list_rooms(self):
        return ",\n".join(self.rooms)

    def generate_rooms(self, rooms_number):
        for i in range(rooms_number):
            room = Room()
            self.rooms[room.name] = room
    
    def get_room(self, room_name):
        return self.rooms[room_name]


