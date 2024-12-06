import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Status(str, Enum):
    success = "success"
    error = "error"


class MsgResponse(BaseModel):
    msg: str
    status: Optional[Status] = None
    timestamp: datetime.datetime = datetime.datetime.now()
