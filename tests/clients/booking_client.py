from tests.config import TIMEOUT, BASE_URL

class BookingClient:
    def __init__(self, session, base_url=BASE_URL, timeout=TIMEOUT):
        self.session = session
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def create(self, payload):
        return self.session.post(
            f'{self.base_url}/bookings',
            json=payload,
            timeout=TIMEOUT)
        

    def get(self, booking_id):
        return self.session.get(
            f'{self.base_url}/booking/{booking_id}',
            timeout=TIMEOUT
        )

    def health(self):
        return self.session.get(f'{self.base_url}/health', timeout=TIMEOUT)