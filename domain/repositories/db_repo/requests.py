from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from domain.repositories.db_repo.reservation import TopchanReservationDBRepo
from domain.repositories.db_repo.topchan import TopchanDBRepo
from domain.repositories.db_repo.user import UserDBRepo


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession

    @property
    def users(self) -> UserDBRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return UserDBRepo(self.session)

    @property
    def topchans(self) -> TopchanDBRepo:
        return TopchanDBRepo(self.session)

    @property
    def reservations(self) -> TopchanReservationDBRepo:
        return TopchanReservationDBRepo(self.session)
