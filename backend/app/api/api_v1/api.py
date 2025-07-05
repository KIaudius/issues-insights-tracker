from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, issues, comments, attachments, stats

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(issues.router, prefix="/issues", tags=["issues"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(attachments.router, prefix="/attachments", tags=["attachments"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
