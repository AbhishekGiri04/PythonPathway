from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, set[WebSocket]] = defaultdict(set)

    async def connect(self, room_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[room_id].add(websocket)

    def disconnect(self, room_id: int, websocket: WebSocket) -> None:
        self.active_connections[room_id].discard(websocket)

    async def broadcast(self, room_id: int, payload: dict) -> None:
        for connection in list(self.active_connections[room_id]):
            await connection.send_json(payload)


chat_manager = ConnectionManager()
