import datetime

from sqlalchemy import DECIMAL, BIGINT, BOOLEAN, TIMESTAMP, String
from sqlalchemy.orm import Mapped, mapped_column

from data.infrastructure.database.models import Base


class TapchanDBModel(Base):
    __tablename__ = "tapchans"

    tapchan_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    reservation_id: Mapped[int] = mapped_column(BIGINT, primary_key=False, autoincrement=False, nullable=True)
    name: Mapped[str] = mapped_column(String(128), nullable=True, default="")
    cost_per_hour: Mapped[float] = mapped_column(DECIMAL(precision=16, scale=4), default=0, nullable=False,
                                                 autoincrement=False)
    longitude: Mapped[int] = mapped_column(DECIMAL(precision=24, scale=24), default=0, nullable=False,
                                           autoincrement=False)
    latitude: Mapped[int] = mapped_column(DECIMAL(precision=24, scale=24), default=0, nullable=False,
                                          autoincrement=False)


class TapchanReservationDBModel(Base):
    __tablename__ = "tapchan_reservations"

    reservation_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    tapchan_id: Mapped[int] = mapped_column(BIGINT, primary_key=False, autoincrement=False)
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=False, autoincrement=False)
    user_phone: Mapped[str] = mapped_column(String(25), nullable=False)
    check_in: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=False)
    check_out: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, autoincrement=False)
