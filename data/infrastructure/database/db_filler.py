from typing import Dict, List

from sqlalchemy import Connection, insert

from data.infrastructure.database.models import TopchanDBModel


class DBFiller:
    _connection: Connection

    _topchans: List[Dict] = [
        {
            "id": 1,
            "name": "1",
            "cost_per_hour": 15000,
            "latitude": 43.34,
            "longitude": 43.34,
        },
        {
            "id": 2,
            "name": "2",
            "cost_per_hour": 18000,
            "latitude": 43.34,
            "longitude": 43.34,
        },
        {
            "id": 3,
            "name": "3",
            "cost_per_hour": 15000,
            "latitude": 43.34,
            "longitude": 43.34,
        },
        {
            "id": 4,
            "name": "4",
            "cost_per_hour": 25000,
            "latitude": 43.34,
            "longitude": 43.34,
        },
    ]

    def __init__(
            self,
            connection: Connection
    ):
        self._connection = connection

    def add_topchans(self):
        for topchan in self._topchans:
            self._connection.execute(
                insert(TopchanDBModel)
                .values(
                    topchan_id=topchan.get("id"),
                    name=topchan.get("name"),
                    cost_per_hour=topchan.get("cost_per_hour"),
                    longitude=topchan.get("longitude"),
                    latitude=topchan.get("latitude"),
                )
            )

