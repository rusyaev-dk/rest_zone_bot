from typing import Optional

from sqlalchemy import select, func, update, and_
from sqlalchemy.dialects.postgresql import insert

from data.infrastructure.database.models import UserDBModel
from domain.repositories.db_repo.base import BaseRepo


class UserDBRepo(BaseRepo):
    async def add_user(
            self,
            telegram_id: int,
            full_name: str,
            language: str,
            phone: str = None,
            username: Optional[str] = None,
    ) -> UserDBModel:
        stmt = (
            insert(UserDBModel)
            .values(
                telegram_id=telegram_id,
                full_name=full_name,
                language=language,
                username=username,
                phone=phone,
            )
            .on_conflict_do_update(
                index_elements=[UserDBModel.telegram_id],
                set_={
                    "full_name": full_name,
                    "language": language,
                    "username": username
                }
            )
            .returning(UserDBModel)
        )
        result = await self.session.execute(stmt)

        await self.session.commit()
        return result.scalar_one()

    async def get_user(
            self,
            telegram_id: int
    ) -> UserDBModel:
        stmt = select(UserDBModel).where(UserDBModel.telegram_id == telegram_id)
        result = await self.session.scalar(stmt)
        return result

    async def get_user_language_code(
            self,
            telegram_id: int
    ) -> str:
        stmt = select(UserDBModel.language).where(UserDBModel.telegram_id == telegram_id)
        result = await self.session.scalar(stmt)
        return result

    async def get_all_users(
            self,
            language_code: str = None
    ):
        if language_code:
            stmt = select(UserDBModel).where(UserDBModel.language == language_code)
        else:
            stmt = select(UserDBModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_users_count(self) -> int:
        stmt = select(func.count(UserDBModel.telegram_id))
        result = await self.session.scalar(stmt)
        return result

    async def get_active_users_count(self) -> int:
        stmt = select(func.count(UserDBModel.telegram_id)).where(UserDBModel.is_active == True)
        result = await self.session.scalar(stmt)
        return result

    async def get_users_count_by_language(self, language_code: str) -> int:
        stmt = select(func.count(UserDBModel.telegram_id)).where(
            and_(
                UserDBModel.language == language_code,
                UserDBModel.is_active == True
            )
        )
        result = await self.session.scalar(stmt)
        return result

    async def update_user_phone(
            self,
            telegram_id: int,
            phone: str,
    ):
        stmt = update(UserDBModel).where(UserDBModel.telegram_id == telegram_id).values(phone=phone)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_user_language(
            self,
            telegram_id: int,
            language_code: str,
    ):
        stmt = update(UserDBModel).where(UserDBModel.telegram_id == telegram_id).values(language=language_code)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_user_active_status(
            self,
            telegram_id: int,
            is_active: bool,
    ):
        stmt = update(UserDBModel).where(UserDBModel.telegram_id == telegram_id).values(is_active=is_active)
        await self.session.execute(stmt)
        await self.session.commit()
