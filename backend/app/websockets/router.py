from fastapi import APIRouter
from app.websockets.routes import router as ws_routes

# Create WebSocket router
websocket_router = APIRouter()

# Include WebSocket routes
websocket_router.include_router(ws_routes, prefix="/ws")
