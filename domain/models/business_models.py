import datetime

from domain.exceptions import IncorrectReservationData, IncorrectCostPerHour


class TopchanReservationModel:
    check_in: datetime
    check_out: datetime
    topchan_id: int
    user_phone: str
    user_id: int

    def __init__(
            self,
            topchan_id: int,
            user_id: int,
            user_phone: str,
            check_in: datetime,
            check_out: datetime,
    ):
        if check_in == check_out or check_out < check_in:
            raise IncorrectReservationData
        self.topchan_id = topchan_id
        self.user_id = user_id
        self.user_phone = user_phone
        self.check_in = check_in
        self.check_out = check_out


class TopchanModel:
    topchan_id: int
    name: str
    longitude: float
    latitude: float

    def __init__(
            self,
            topchan_id: int,
            name: str,
            cost_per_day: float,
            longitude: float,
            latitude: float,
    ):
        if cost_per_day < 0:
            raise IncorrectCostPerHour
        self.topchan_id = topchan_id
        self.name = name
        self.cost_per_day = cost_per_day
        self.longitude = longitude
        self.latitude = latitude

    def change_cost_per_hour(self, cost_per_day: float):
        if cost_per_day < 0:
            raise IncorrectCostPerHour
        self.cost_per_day = cost_per_day

    def change_location(
            self,
            longitude: float,
            latitude: float
    ):
        self.longitude = longitude
        self.latitude = latitude
