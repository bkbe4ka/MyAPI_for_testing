from fastapi import FastAPI, Depends, HTTPException, status, Request
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.exception_handler(DataError)
def handle_data_error(request, exc):
    return JSONResponse(
        status_code = 422,
        content={"detail": [
                {
                    "loc": ["body"],
                    "msg": "Invalid data or database constraints",
                    "type": "value_error",
                }
            ]}
    )

@app.post(
        '/bookings',
        response_model = BookingResponse,
        status_code = status.HTTP_201_CREATED,
        summary = 'Create booking',
        description = (
            "Создаёт новую бронь.\n\n"
            "**Ограничение, не выразимое в JSON Schema:** "
            "`checkout` должен быть строго больше `checkin`. "
            "При нарушении возвращается 422."
        ),
        responses={422: {'description': 'Booking not found'}}
)

@app.get(
    '/bookings/{booking_id}',
    response_model = BookingResponse,
    responses = {404: {'description': 'Booking not found'}}
)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if booking is None:
        raise HTTPException(status_code = 404, detail='Booking not found')
    return booking

@app.exception_handler(SQLAlchemyError)
def handler_db_error(request, exc):
    return JSONResponse(status_code=422, content={"detail": [
                {
                    "loc": ["body"],
                    "msg": "Invalid data",
                    "type": "value_error",
                }
            ]})



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



@app.middleware("http")
async def add_allow_header(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 405 and "allow" not in response.headers:
        response.headers["Allow"] = "GET, POST, OPTIONS"
    return response


