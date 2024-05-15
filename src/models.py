from datetime import datetime, timezone
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from src.database import Model
import email_validator


class Doctor(Model):
    __tablename__ = 'doctors'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(64))

    visits: Mapped[List['Visit'] | None] = relationship(back_populates='doctor')


class User(Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    email: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column(String(256))
    registration_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    visits: Mapped[List['Visit'] | None] = relationship(back_populates='patient')

    @validates('email')
    def validate_email(self, key, email):
        return email_validator.validate_email(email)


class Visit(Model):
    __tablename__ = 'visits'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime]
    doctor_id: Mapped[int] = mapped_column(ForeignKey(Doctor.id), index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)

    doctor: Mapped["Doctor"] = relationship(back_populates="visits")
    patient: Mapped["User"] = relationship(back_populates="visits")