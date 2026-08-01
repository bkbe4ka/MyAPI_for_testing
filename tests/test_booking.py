import pytest

from models.booking import BookingResponse
from app.models import Booking


def test_create_booking_return_2xx(booking_client, valid_payload):
    response = booking_client.create(valid_payload)
    assert response.status_code == 201, response.text

    body = BookingResponse.model_validate(response.json())
    assert body.id
    assert body.firstname == valid_payload['firstname']


def test_created_booking_is_persisted(booking_client, db_session, valid_payload):
    valid_payload['checkout'] = valid_payload['checkin']

    response = booking_client.create(valid_payload)
    assert response.status_code == 422, response.text

    assert db_session.query(Booking).count() == 0


@pytest.mark.parametrize(
    'missing_field',
    ['firstname', 'lastname', 'totalprice', 'depositpaid', 'checkin', 'checkout'])
def test_create_booking_without_required_field_returns_422(booking_client, valid_payload, missing_field):
    del valid_payload[missing_field]

    response = booking_client.create(valid_payload)
    assert response.status_code == 422, response.text


def test_create_booking_rejects_unknown_field(booking_client, valid_payload):
    valid_payload['is_admin'] = True
    resposne = booking_client.create(valid_payload)
    assert resposne.status_code == 422, resposne.text

def test_nonexist_booking_returns_404(booking_client):
    response = booking_client.get(999999999999999999999)

    assert response.status_code == 404, response.text

def test_create_booking_with_out_of_range_totalprice(booking_client, valid_payload):
    valid_payload['totalprice'] = 2832897238042370239847034892340897

    response = booking_client.create(valid_payload)

    assert response.status_code == 422, response.text

def test_create_booking_with_null_byte_returns_422(booking_client, valid_payload):
    valid_payload["firstname"] = "dfgdfgdfg\x00Test"

    response = booking_client.create(valid_payload)

    assert response.status_code == 422, response.text