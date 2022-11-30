from urllib import request
from pathlib import Path
from fastapi import FastAPI, Depends, Request, HTTPException
import uvicorn
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import models
from database import Base, engine, SessionLocal
import query_crud
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "static"))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

#
# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(engine)


@app.get("/schedule")
async def get_free_time_slots(db: Session = Depends(get_db)):
    return await query_crud.get_time_slot(db)


@app.post("/schedule")
async def create_time_slot(time_slot: models.RequestBookingTimeSlot, db: Session = Depends(get_db)):
    return await query_crud.create_time_slot(db, time_slot)


@app.put("/schedule/{id}")
async def update_booking_slot(id: int, request_body: models.RequestBookingTimeSlot, db: Session = Depends(get_db)):
    return await query_crud.update_time_slot(db, id, request_body)

@app.get("/hi")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
