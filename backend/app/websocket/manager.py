"""Production-ready WebSocket Connection Manager foundation."""

from typing import Dict, List, Any
from fastapi import WebSocket
from loguru import logger


class ConnectionManager:
    """Manages active WebSocket client connections and message broadcasting."""

    def __init__(self) -> None:
        """Initialize active connection tracking stores."""
        self.active_connections: List[WebSocket] = []
        self.client_metadata: Dict[WebSocket, Dict[str, Any]] = {}

    async def connect(self, websocket: WebSocket, client_id: str = "anonymous") -> None:
        """Accept an incoming WebSocket connection and register it.

        Args:
            websocket (WebSocket): Incoming connection instance.
            client_id (str): Optional identifier for client socket.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        self.client_metadata[websocket] = {"client_id": client_id, "connected_at": websocket.headers.get("date")}
        logger.info(f"WebSocket client connected: {client_id} (Active connections: {len(self.active_connections)})")

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove a disconnected WebSocket connection from active pool.

        Args:
            websocket (WebSocket): Connection instance to remove.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            client_info = self.client_metadata.pop(websocket, {})
            client_id = client_info.get("client_id", "unknown")
            logger.info(f"WebSocket client disconnected: {client_id} (Active connections: {len(self.active_connections)})")

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        """Send a text message to a specific WebSocket client.

        Args:
            message (str): Text message body.
            websocket (WebSocket): Target client socket.
        """
        await websocket.send_text(message)

    async def send_json(self, data: dict, websocket: WebSocket) -> None:
        """Send structured JSON payload to a specific WebSocket client.

        Args:
            data (dict): JSON serializable dictionary.
            websocket (WebSocket): Target client socket.
        """
        await websocket.send_json(data)

    async def broadcast_text(self, message: str) -> None:
        """Broadcast text message to all active WebSocket connections.

        Args:
            message (str): Message to broadcast.
        """
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception as exc:
                logger.warning(f"Error broadcasting message to client: {exc}")
                self.disconnect(connection)

    async def broadcast_json(self, data: dict) -> None:
        """Broadcast JSON data to all active WebSocket connections.

        Args:
            data (dict): JSON payload to broadcast.
        """
        for connection in list(self.active_connections):
            try:
                await connection.send_json(data)
            except Exception as exc:
                logger.warning(f"Error broadcasting JSON to client: {exc}")
                self.disconnect(connection)

    def active_count(self) -> int:
        """Return the count of currently connected clients."""
        return len(self.active_connections)


# Singleton manager instance
ws_manager = ConnectionManager()
