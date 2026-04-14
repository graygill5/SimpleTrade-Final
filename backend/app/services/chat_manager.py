from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.room_connections: dict[int, list[WebSocket]] = defaultdict(list)
        self.user_connections: dict[int, WebSocket] = {}

    async def connect(self, room_id: int, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.room_connections[room_id].append(websocket)
        self.user_connections[user_id] = websocket

    def disconnect(self, room_id: int, user_id: int, websocket: WebSocket):
        if websocket in self.room_connections[room_id]:
            self.room_connections[room_id].remove(websocket)
        self.user_connections.pop(user_id, None)

    async def room_broadcast(self, room_id: int, payload: dict):
        for conn in list(self.room_connections[room_id]):
            await conn.send_json(payload)


chat_manager = ConnectionManager()
