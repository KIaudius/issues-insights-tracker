from typing import Dict, List, Any, Optional
from fastapi import WebSocket
import json
from uuid import UUID

class ConnectionManager:
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[UUID, List[WebSocket]] = {}
        # Store active issue subscriptions by user_id
        self.issue_subscriptions: Dict[UUID, List[int]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: UUID):
        """Connect a user's WebSocket"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: UUID):
        """Disconnect a user's WebSocket"""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    def subscribe_to_issue(self, user_id: UUID, issue_id: int):
        """Subscribe user to issue updates"""
        if user_id not in self.issue_subscriptions:
            self.issue_subscriptions[user_id] = []
        if issue_id not in self.issue_subscriptions[user_id]:
            self.issue_subscriptions[user_id].append(issue_id)
    
    def unsubscribe_from_issue(self, user_id: UUID, issue_id: int):
        """Unsubscribe user from issue updates"""
        if user_id in self.issue_subscriptions:
            if issue_id in self.issue_subscriptions[user_id]:
                self.issue_subscriptions[user_id].remove(issue_id)
            if not self.issue_subscriptions[user_id]:
                del self.issue_subscriptions[user_id]
    
    async def send_personal_message(self, message: Any, user_id: UUID):
        """Send message to a specific user"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)
    
    async def broadcast_to_issue_subscribers(self, message: Any, issue_id: int):
        """Send message to all subscribers of an issue"""
        for user_id, subscriptions in self.issue_subscriptions.items():
            if issue_id in subscriptions and user_id in self.active_connections:
                await self.send_personal_message(message, user_id)
    
    async def broadcast(self, message: Any):
        """Send message to all connected users"""
        for user_id in self.active_connections:
            await self.send_personal_message(message, user_id)

# Create a global connection manager instance
manager = ConnectionManager()
