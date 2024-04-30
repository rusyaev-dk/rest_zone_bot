from typing import List

from sqlalchemy import select, update, and_
from sqlalchemy.dialects.postgresql import insert

from data.infrastructure.database.models import TopchanDBModel
from domain.models.business_models import TopchanModel
from domain.repositories.db_repo.base import BaseRepo


class TopchanDBRepo(BaseRepo):
    async def add_topchan(
            self,
            cost_per_hour: float,
            name: str,
            longitude: float,
            latitude: float,
            topchan_id: int = None,
    ):
        if not topchan_id:
            topchan_id = await self.get_last_topchan_id()
        stmt = (
            insert(TopchanDBModel)
            .values(
                topchan_id=topchan_id,
                name=name,
                cost_per_hour=cost_per_hour,
                longitude=longitude,
                latitude=latitude,
            ).on_conflict_do_nothing()
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_last_topchan_id(self) -> int:
        stmt = select(TopchanDBModel).order_by(TopchanDBModel.topchan_id.desc())
        result = await self.session.scalar(stmt)
        if not result:
            result = 0
        return result

    async def get_topchan(
            self,
            topchan_id: int
    ) -> TopchanModel:
        stmt = select(TopchanDBModel).where(TopchanDBModel.topchan_id == topchan_id)
        topchan_db = await self.session.scalar(stmt)

        topchan: TopchanModel = TopchanModel(
            topchan_id=topchan_db.topchan_id,
            name=topchan_db.name,
            cost_per_hour=topchan_db.cost_per_hour,
            latitude=topchan_db.latitude,
            longitude=topchan_db.longitude,
        )
        return topchan

    async def get_all_topchans(
            self,
    ) -> List[TopchanModel]:
        stmt = select(TopchanDBModel)
        topchans_db_models = await self.session.scalars(stmt)

        res_topchans = []
        for topchan_db in topchans_db_models:
            res_topchans.append(
                TopchanModel(
                    topchan_id=topchan_db.topchan_id,
                    name=topchan_db.name,
                    cost_per_hour=topchan_db.cost_per_hour,
                    latitude=topchan_db.latitude,
                    longitude=topchan_db.longitude,
                )
            )
        return res_topchans

    # async def update_tapchan(
    #         self,
    #         *clauses,
    #         **values,
    # ):
    #     stmt = update(TapchanDBModel).where(*clauses).values(**values)
    #     await self.session.execute(stmt)
    #     await self.session.commit()
