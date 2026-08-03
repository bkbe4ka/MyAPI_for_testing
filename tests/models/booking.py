from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class BookingResponse(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

    id: int
    firstname: str = Field(min_length=1, max_length=50)
    lastname: str = Field(min_length=1, max_length=50)
    totalprice: int = Field(ge=0, le=2_147_483_647)
    depositpaid: bool
    checkin: date = Field(strict=False)
    checkout: date = Field(strict=False)
    additionalneeds: str | None = Field(default=None, max_length=200)
