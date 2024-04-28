

class ForRentException(Exception):
    pass


class IncorrectReservationData(ForRentException):
    pass


class IncorrectCostPerHour(ForRentException):
    pass
