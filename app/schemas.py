from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator


class BookingCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    firstname: str = Field(min_length = 1, max_length = 50)
    lastname: str = Field(min_length = 1, max_length = 50)
    totalprice: int = Field(ge=0)
    depositpaid: bool
    checkin: date
    checkout: date
    additionalneeds: str | None = Field(default=None, max_length=200)

    @model_validator(mode='after')
    def checkout_after_ckeckin(self):
        if self.checkout <= self.checkin:
            raise ValueError('Checkout must be after checkin')
        return self


    @field_validator('firstname', 'lastname', 'additionalneeds')
    @classmethod
    def no_null_bytes(cls, v: str | None) -> str | None:
        if v is not None and '\x00' in v:
            raise ValueError('Field must not contain NUL characters')
        return v

class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    firstname: str
    lastname: str
    totalprice: int = Field(ge=0, le=2_147_483_647)
    depositpaid: bool
    checkin: date
    checkout: date
    additionalneeds: str | None
