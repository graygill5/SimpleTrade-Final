from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_rooms: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept()
        self.active_rooms[room].append(websocket)

    def disconnect(self, room: str, websocket: WebSocket):
        if websocket in self.active_rooms[room]:
            self.active_rooms[room].remove(websocket)

    async def broadcast(self, room: str, message: str):
        for connection in list(self.active_rooms[room]):
            await connection.send_text(message)


chat_manager = ConnectionManager()
