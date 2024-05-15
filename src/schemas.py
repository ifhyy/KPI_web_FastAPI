from datetime import datetime

from pydantic import BaseModel


class VisitBase(BaseModel):
    date: datetime
