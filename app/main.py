from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import check_connection, SessionLocal
from app.models import Booking
from app.schemas import BookingCreate, BookingResponse
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError
from sqlalchemy.exc import SQLAlchemyError


app = FastAPI(
    title = 'Booking API',
    version = '0.1.0'
)

@app.exception_handler(DataError)
def handle_data_error(request, exc):
    return JSONResponse(
        status_code = 422,
        content={'detail': 'Invalid data or database constraints'}
    )


@app.exception_handler(SQLAlchemyError)
def handler_db_error(request, exc):
    return JSONResponse(status_code=422, content={'detail': 'Invalid data'})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/health')
def health():
    return {'status': 'OK', 'database': check_connection()}


@app.post('/bookings', response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    booking = Booking(**payload.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@app.get('bookings/{booking_id}', response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail='Booking not found')
    return booking
