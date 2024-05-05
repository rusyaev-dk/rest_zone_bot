import datetime

from sqlalchemy import DECIMAL, BIGINT, BOOLEAN, TIMESTAMP, String
from sqlalchemy.orm import Mapped, mapped_column

from data.infrastructure.database.models import Base


class TopchanDBModel(Base):
    __tablename__ = "topchans"

    topchan_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(128), nullable=True, default="")
    cost_per_day: Mapped[float] = mapped_column(DECIMAL(precision=16, scale=4), default=0, nullable=False,
                                                autoincrement=False)
    longitude: Mapped[int] = mapped_column(DECIMAL(precision=16, scale=4), default=0, nullable=False,
                                           autoincrement=False)
    latitude: Mapped[int] = mapped_column(DECIMAL(precision=16, scale=4), default=0, nullable=False,
                                          autoincrement=False)


class TopchanReservationDBModel(Base):
    __tablename__ = "topchan_reservations"

    reservation_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    topchan_id: Mapped[int] = mapped_column(BIGINT, primary_key=False, autoincrement=False)
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=False, autoincrement=False)
    user_phone: Mapped[str] = mapped_column(String(25), nullable=False)
    check_in: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=False)
    check_out: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=False)
