from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingResponse(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

    id: int
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    checkin: date
    checkout: date
    additionalneeds: str | None = None
    