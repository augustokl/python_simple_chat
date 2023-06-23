import asyncio

import websockets
from room import RoomManager, Room

room_manager = RoomManager()
room_manager.generate_rooms(3)

allowed_commands = {"\\all": "sent_broadcast", "\\private": "sent_private_message", "\\exit": "exit_room"}

async def handler(websocket):
    room: Room = None
    return_message = None

    await websocket.send(f"Type the room you want to join: {room_manager.list_rooms()}")


    async for message in websocket:
        if room is None:
            room = room_manager.get_room(room_name=message)
            room.join_room(user_socket=websocket)

        splitted_message = message.split(' ', maxsplit=1)

        if splitted_message and splitted_message[0] in allowed_commands:
            command = getattr(room, allowed_commands[splitted_message[0]])
            exited = command(splitted_message[1])

            if exited: 
                await websocket.send(f"Type the room you want to join: {room_manager.list_rooms()}")
                room = None

async def main():
    async with websockets.serve(handler, "", 8001):
        try:
            await asyncio.Future()  # run forever
        except Exception as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(main())