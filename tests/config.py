import os


BASE_URL = os.getenv('API_BASE_URl', 'http://localhost:8000')
TIMEOUT = 10
DATABASE_URL = (
    'TEST_DATABASE_URL',
    'postgresql+psycopg2://booking:booking@localhost:5432/booking'
)

