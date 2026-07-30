from sqlalchemy import Boolean, CheckConstraint, Date, Integer, String

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date

class Base(DeclarativeBase):
    pass

class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    totalprice: Mapped[int] = mapped_column(Integer, nullable=False)
    depositpaid: Mapped[bool] = mapped_column(Boolean, nullable=False)
    checkin: Mapped[date] = mapped_column(Date, nullable=False)
    checkout: Mapped[date] = mapped_column(Date, nullable=False)
    additionalneeds: Mapped[str | None] = mapped_column(String(200), nullable=True)

    __table_args__ = (CheckConstraint('totalprice >=0', name='ck_totalprice_non_negative'),
        CheckConstraint('checkout > checkin', name='ck_checkout_after_checkin'))
    