from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validation


class BookingCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    firstname: str = Field(min_length = 1, max_length = 50)
    lastname: str = Field(min_length = 1, max_length = 50)
    totalprice: int = Field(ge=0)
    depositpaid: bool
    checkin: date
    checkout: date
    additionalneeds: str | None = Field(default=None, max_length=200)

    @model_validation(mode='after')
    def checkout_after_ckeckin(self):
        if self.checkout <= self.checkin:
            raise ValueError('Checkout must be after checkin')
        return self

class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    checkin: date
    checkout: date
    additionalneeds: str | None
