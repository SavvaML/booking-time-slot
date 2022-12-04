from fastapi import HTTPException
from sqlalchemy import update, delete
from sqlalchemy.orm import Session
import models


async def get_time_slot(db: Session):
    time_slots = db.query(models.BookingTimeSlot).all()
    return time_slots


async def get_time_slot_by_date(db: Session, date: str):
    time_slots = db.query(models.BookingTimeSlot).where(models.BookingTimeSlot.date == date).all()
    return time_slots

async def create_time_slot(db: Session, time_slot):
    db_item = models.BookingTimeSlot(date=time_slot.date,
                                     start_booking=time_slot.start_booking,
                                     end_booking=time_slot.end_booking,
                                     description=time_slot.description,
                                     fist_name_client=time_slot.fist_name_client,
                                     last_name_client=time_slot.last_name_client,
                                     email=time_slot.email)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


async def update_time_slot(db: Session, time_slot_id, request):
    sql_request = update(models.BookingTimeSlot).where(
        models.BookingTimeSlot.id == time_slot_id
            ).values(date=request.date,
                     start_booking=request.start_booking,
                     end_booking=request.end_booking,
                     description=request.description,
                     fist_name_client=request.fist_name_client,
                     last_name_client=request.last_name_client,
                     email=request.email
                     )
    db.execute(sql_request)
    db.commit()
    return request
