from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class BookingResponse(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

    id: int
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    checkin: date = Field(strict=False)
    checkout: date = Field(strict=False)
    additionalneeds: str | None = None
