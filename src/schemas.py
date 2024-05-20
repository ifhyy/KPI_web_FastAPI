from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class VisitBase(BaseModel):
    date: datetime
    doctor_id: int
    patient_id: int


class VisitIn(VisitBase):
    pass


class VisitOut(BaseModel):
    id: int


class DoctorBase(BaseModel):
    full_name = str
    license_number = str


class DoctorIn(DoctorBase):
    pass


class DoctorOut(DoctorBase):
    id: int
    visits: Optional[List[VisitOut]]


class UserBase(BaseModel):
    pass
