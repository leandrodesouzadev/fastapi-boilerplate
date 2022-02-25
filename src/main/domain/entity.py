import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Entity(BaseModel):

    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
