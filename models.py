from pydantic.class_validators import Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
from database import Base
from pydantic import BaseModel


class BookingTimeSlot(Base):
    __tablename__ = "booking_time_slot"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, primary_key=False)
    start_booking = Column(String, primary_key=False)
    end_booking = Column(String, primary_key=False)
    description = Column(String, primary_key=False)
    fist_name_client = Column(String, primary_key=False)
    last_name_client = Column(String, primary_key=False)
    email = Column(String, primary_key=False)


class RequestBookingTimeSlot(BaseModel):
    date: str
    start_booking: str
    end_booking: str
    description: str
    fist_name_client: str
    last_name_client: str
    email: str

    class Config:
        orm_mode = True


