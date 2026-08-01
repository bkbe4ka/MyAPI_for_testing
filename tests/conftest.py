import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from clients.booking_client import BookingClient
from config import DATABASE_URL

from app.models import Booking


@pytest.fixture
def session():
    s = requests.Session()
    s.trust_env = False
    yield
    s.close()

@pytest.fixture
def booking_client(session):
    return BookingClient(session)

@pytest.fixture(scope='session')
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture(autouse=True)
def clean_db(db_session):
    db_session.query(Booking).delete()
    db_session.commit()
    yield

@pytest.fixture
def valid_payload():
    return {
        "firstname": "dfgdfgdfg",
        "lastname": "dfgdgdfgdgdfgdfg",
        "totalprice": 150,
        "depositpaid": True,
        "checkin": "2026-03-01",
        "checkout": "2026-03-05",
        "additionalneeds": "Breakfast"
    }