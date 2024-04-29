import datetime

from domain.exceptions import IncorrectReservationData, IncorrectCostPerHour


class TapchanReservationModel:
    check_in: datetime
    check_out: datetime
    tapchan_id: int
    user_phone: str
    user_id: int

    def __init__(
            self,
            tapchan_id: int,
            user_id: int,
            user_phone: str,
            check_in: datetime,
            check_out: datetime,
    ):
        if check_in == check_out or check_out < check_in:
            raise IncorrectReservationData
        self.tapchan_id = tapchan_id
        self.user_id = user_id
        self.user_phone = user_phone
        self.check_in = check_in
        self.check_out = check_out


class TapchanModel:
    tapchan_id: int
    name: str
    longitude: float
    latitude: float

    def __init__(
            self,
            tapchan_id: int,
            name: str,
            cost_per_hour: float,
            longitude: float,
            latitude: float,
            reservation: TapchanReservationModel = None,
    ):
        if cost_per_hour < 0:
            raise IncorrectCostPerHour
        self.tapchan_id = tapchan_id
        self.name = name
        self.cost_per_hour = cost_per_hour
        self.longitude = longitude
        self.latitude = latitude
        self.reservation = reservation

    def change_cost_per_hour(self, cost_per_hour: float):
        if cost_per_hour < 0:
            raise IncorrectCostPerHour
        self.cost_per_hour = cost_per_hour

    def update_reservation(self, reservation: TapchanReservationModel):
        self.reservation = reservation

    def change_location(
            self,
            longitude: float,
            latitude: float
    ):
        self.longitude = longitude
        self.latitude = latitude
