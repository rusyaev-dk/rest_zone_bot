import calendar
import datetime
from typing import List

from sqlalchemy import select, update, and_, extract
from sqlalchemy.dialects.postgresql import insert

from data.infrastructure.database.models import TopchanReservationDBModel
from domain.models.business_models import TopchanReservationModel
from domain.repositories.db_repo.base import BaseRepo
from tgbot.services.micro_functions import generate_int_id


class TopchanReservationDBRepo(BaseRepo):
    async def add_reservation(
            self,
            topchan_id: int,
            user_id: int,
            user_phone: str,
            check_in: datetime,
            check_out: datetime
    ):
        stmt = (
            insert(TopchanReservationDBModel)
            .values(
                reservation_id=generate_int_id(),
                topchan_id=topchan_id,
                user_id=user_id,
                user_phone=user_phone,
                check_in=check_in,
                check_out=check_out,
            )
        ).on_conflict_do_nothing()

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_reservation(
            self,
            reservation_id: int,
    ) -> TopchanReservationModel:
        stmt = select(TopchanReservationDBModel).where(TopchanReservationDBModel.reservation_id == reservation_id)
        result = await self.session.scalar(stmt)
        reservation = TopchanReservationModel(
            topchan_id=result.topchan_id,
            user_id=result.user_id,
            user_phone=result.user_phone,
            check_in=result.check_in,
            check_out=result.check_out,
        )
        return reservation

    async def get_relevance_topchan_reservations(
            self,
            topchan_id: int,
    ) -> List[TopchanReservationModel]:
        stmt = select(TopchanReservationDBModel).where(TopchanReservationDBModel.topchan_id == topchan_id)
        reservations_db_models = await self.session.scalars(stmt)

        res_reservations = []
        for reservation_db in reservations_db_models:
            res_reservations.append(
                TopchanReservationModel(
                    topchan_id=reservation_db.topchan_id,
                    user_id=reservation_db.user_id,
                    user_phone=reservation_db.user_phone,
                    check_in=reservation_db.check_in,
                    check_out=reservation_db.check_out,
                )
            )
        return res_reservations

    async def get_topchan_reservations_by_month(
            self,
            topchan_id: int,
            month: int,
    ) -> List[TopchanReservationModel]:
        current_year = datetime.datetime.now().year

        # Определяем начало и конец месяца
        start_of_month = datetime.date(current_year, month, 1)
        end_of_month = datetime.date(current_year, month, calendar.monthrange(current_year, month)[1])

        stmt = select(TopchanReservationDBModel).where(
            and_(
                TopchanReservationDBModel.topchan_id == topchan_id,
                extract('month', TopchanReservationDBModel.check_in) == month,
                extract('year', TopchanReservationDBModel.check_in) == current_year,  # Используем текущий год
                TopchanReservationDBModel.check_in >= start_of_month,
                TopchanReservationDBModel.check_in <= end_of_month
            )
        )
        reservations_db_models = await self.session.scalars(stmt)

        res_reservations = []
        for reservation_db in reservations_db_models:
            res_reservations.append(
                TopchanReservationModel(
                    topchan_id=reservation_db.topchan_id,
                    user_id=reservation_db.user_id,
                    user_phone=reservation_db.user_phone,
                    check_in=reservation_db.check_in,
                    check_out=reservation_db.check_out,
                )
            )
        return res_reservations
