from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(from_attributes=True)

class BaseAPIResponse(BaseSchema):
    """Base API response schema"""
    success: bool = True
    message: Optional[str] = None
