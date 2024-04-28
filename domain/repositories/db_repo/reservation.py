import datetime

from sqlalchemy import select, func, update, and_
from sqlalchemy.dialects.postgresql import insert

from data.infrastructure.database.models import TapchanReservationDBModel
from domain.models.business_models import TapchanReservationModel
from domain.repositories.db_repo.base import BaseRepo
from tgbot.services.micro_functions import generate_int_id


class TapchanReservationDBRepo(BaseRepo):
    async def add_reservation(
            self,
            tapchan_id: int,
            check_in: datetime,
            check_out: datetime
    ):
        stmt = (
            insert(TapchanReservationDBModel)
            .values(
                reservation_id=generate_int_id(),
                tapchan_id=tapchan_id,
                check_in=check_in,
                check_out=check_out,
            )
        ).on_conflict_do_nothing()

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_reservation(
            self,
            reservation_id: int,
    ) -> TapchanReservationModel:
        stmt = select(TapchanReservationDBModel).where(TapchanReservationDBModel.reservation_id == reservation_id)
        result = await self.session.scalar(stmt)
        reservation = TapchanReservationModel(
            tapchan_id=result.tapchan_id,
            check_in=result.check_in,
            check_out=result.check_out,
        )
        return reservation

    async def update_reservation(
            self,
            *clauses,
            **values,
    ):
        stmt = update(TapchanReservationDBModel).where(*clauses).values(**values)
        await self.session.execute(stmt)
        await self.session.commit()
