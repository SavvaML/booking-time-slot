from urllib import request
from pathlib import Path
from fastapi import FastAPI, Depends, Request, HTTPException
import uvicorn
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
import utils
import models
from database import Base, engine, SessionLocal
import query_crud
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(engine)


@app.get("/booking_time_slot")
async def get_booking_time_slots(db: Session = Depends(get_db)):
    return await query_crud.get_time_slot(db)

@app.get("/schedule/{date}")
async def get_free_time_slots(date, db: Session = Depends(get_db)):
    booking = await query_crud.get_time_slot_by_date(db, date)
    booking_time = [i.start_booking for i in booking]
    time_slot = [i for i in utils.get_time_slote() if i[0] not in booking_time]
    return time_slot

@app.post("/schedule")
async def create_time_slot(time_slot: models.RequestBookingTimeSlot, db: Session = Depends(get_db)):
    return await query_crud.create_time_slot(db, time_slot)


@app.put("/schedule/{id}")
async def update_booking_slot(id: int, request_body: models.RequestBookingTimeSlot, db: Session = Depends(get_db)):
    return await query_crud.update_time_slot(db, id, request_body)



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
