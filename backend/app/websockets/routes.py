from typing import Any, Dict, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json

from app.db.database import SessionLocal
from app.core.security import decode_jwt_token
from app.websockets.manager import manager
from app.crud.issue_crud import get_issue
from app.models.user import User
from app.models.issue import Issue

router = APIRouter()

async def get_current_user_from_token(token: str) -> Optional[Dict[str, Any]]:
    """Validate JWT token and return user data"""
    try:
        payload = decode_jwt_token(token)
        return payload
    except Exception:
        return None

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    # Wait for authentication message
    await websocket.accept()
    
    try:
        # First message should contain the auth token
        auth_message = await websocket.receive_json()
        token = auth_message.get("token")
        
        if not token:
            await websocket.send_json({"error": "Authentication required"})
            await websocket.close(code=1008)  # Policy violation
            return
        
        # Validate token
        user_data = await get_current_user_from_token(token)
        if not user_data:
            await websocket.send_json({"error": "Invalid authentication token"})
            await websocket.close(code=1008)  # Policy violation
            return
        
        user_id = user_data.get("sub")
        if not user_id:
            await websocket.send_json({"error": "Invalid user ID"})
            await websocket.close(code=1008)  # Policy violation
            return
        
        # Register connection
        await manager.connect(websocket, user_id)
        await websocket.send_json({"message": "Connected successfully"})
        
        # Handle messages
        try:
            while True:
                message = await websocket.receive_json()
                
                # Handle subscription requests
                if message.get("type") == "subscribe":
                    issue_id = message.get("issue_id")
                    if issue_id:
                        # Validate issue exists and user has access
                        db = SessionLocal()
                        try:
                            issue = get_issue(db, issue_id=issue_id)
                            if issue:
                                manager.subscribe_to_issue(user_id, issue_id)
                                await websocket.send_json({
                                    "type": "subscription",
                                    "status": "subscribed",
                                    "issue_id": issue_id
                                })
                            else:
                                await websocket.send_json({
                                    "type": "error",
                                    "message": "Issue not found"
                                })
                        finally:
                            db.close()
                
                # Handle unsubscribe requests
                elif message.get("type") == "unsubscribe":
                    issue_id = message.get("issue_id")
                    if issue_id:
                        manager.unsubscribe_from_issue(user_id, issue_id)
                        await websocket.send_json({
                            "type": "subscription",
                            "status": "unsubscribed",
                            "issue_id": issue_id
                        })
                
                # Handle ping to keep connection alive
                elif message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                
        except WebSocketDisconnect:
            manager.disconnect(websocket, user_id)
    
    except WebSocketDisconnect:
        # Client disconnected before authentication
        pass
    except Exception as e:
        # Handle any other exceptions
        try:
            await websocket.send_json({"error": str(e)})
            await websocket.close()
        except:
            pass

# Helper function to send issue update to subscribers
async def send_issue_update(issue: Issue, update_type: str):
    """Send issue update to all subscribers"""
    message = {
        "type": "issue_update",
        "update_type": update_type,
        "issue": {
            "id": issue.id,
            "title": issue.title,
            "status": issue.status.value,
            "severity": issue.severity.value,
            "updated_at": issue.updated_at.isoformat()
        }
    }
    await manager.broadcast_to_issue_subscribers(message, issue.id)

# Helper function to send comment update to issue subscribers
async def send_comment_update(comment: Any, update_type: str):
    """Send comment update to all issue subscribers"""
    message = {
        "type": "comment_update",
        "update_type": update_type,
        "comment": {
            "id": comment.id,
            "content": comment.content,
            "issue_id": comment.issue_id,
            "user_id": comment.user_id,
            "created_at": comment.created_at.isoformat()
        }
    }
    await manager.broadcast_to_issue_subscribers(message, comment.issue_id)

# Helper function to send attachment update to issue subscribers
async def send_attachment_update(attachment: Any, update_type: str):
    """Send attachment update to all issue subscribers"""
    message = {
        "type": "attachment_update",
        "update_type": update_type,
        "attachment": {
            "id": attachment.id,
            "filename": attachment.filename,
            "issue_id": attachment.issue_id,
            "uploader_id": attachment.uploader_id,
            "created_at": attachment.created_at.isoformat()
        }
    }
    await manager.broadcast_to_issue_subscribers(message, attachment.issue_id)
