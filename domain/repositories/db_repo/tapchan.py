
from sqlalchemy import select, func, update, and_
from sqlalchemy.dialects.postgresql import insert

from data.infrastructure.database.models import TapchanDBModel, TapchanReservationDBModel
from domain.models.business_models import TapchanModel, TapchanReservationModel
from domain.repositories.db_repo.base import BaseRepo


class TapchanDBRepo(BaseRepo):
    async def add_tapchan(
            self,
            cost_per_hour: float,
            name: str,
            longitude: float,
            latitude: float,
            tapchan_id: int = None,
            reservation_id: int = None
    ):
        if not tapchan_id:
            tapchan_id = await self.get_last_tapchan_id()
        stmt = (
            insert(TapchanDBModel)
            .values(
                tapchan_id=tapchan_id,
                name=name,
                reservation_id=reservation_id,
                cost_per_hour=cost_per_hour,
                longitude=longitude,
                latitude=latitude,
            ).on_conflict_do_nothing()
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_last_tapchan_id(self) -> int:
        stmt = select(TapchanDBModel).order_by(TapchanDBModel.tapchan_id.desc())
        result = await self.session.scalar(stmt)
        if not result:
            result = 0
        return result

    async def get_tapchan(
            self,
            tapchan_id: int
    ) -> TapchanModel:
        stmt = select(TapchanDBModel).where(TapchanDBModel.tapchan_id == tapchan_id)
        tapchan_db = await self.session.scalar(stmt)
        stmt = select(TapchanReservationDBModel).where(TapchanReservationDBModel.tapchan_id == tapchan_id)

        reservation_db = await self.session.scalar(stmt)
        reservation = TapchanReservationModel(
            tapchan_id=reservation_db.tapchan_id,
            check_in=reservation_db.check_in,
            check_out=reservation_db.check_out,
        )

        tapchan = TapchanModel(
            tapchan_id=tapchan_db.tapchan_id,
            name=tapchan_db.name,
            cost_per_hour=tapchan_db.cost_per_hour,
            latitude=tapchan_db.latitude,
            longitude=tapchan_db.longitude,
            reservation=reservation,
        )
        return tapchan

    async def update_tapchan(
            self,
            *clauses,
            **values,
    ):
        stmt = update(TapchanDBModel).where(*clauses).values(**values)
        await self.session.execute(stmt)
        await self.session.commit()
