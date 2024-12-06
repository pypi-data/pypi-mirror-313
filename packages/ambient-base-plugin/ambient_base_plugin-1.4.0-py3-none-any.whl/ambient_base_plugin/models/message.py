from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    id: Optional[int] = Field(None, title="Id")
    created_at: Optional[datetime] = Field(
        "2024-04-27T03:22:46.716266", title="Created At"
    )
    topic: str = Field(..., title="Topic")
    message: str = Field(..., title="Message")
    connection_id: Optional[int] = Field(None, title="Connection Id")
    session_id: Optional[int] = Field(None, title="Session Id")
    timestamp: Optional[datetime] = Field(None, title="Timestamp")
