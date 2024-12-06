#
#  Copyright (c) OKB Fifth Generation, 2024.
#
from datetime import datetime


class PredictParams:
    __satellite: int
    __ground_station: int
    __from: datetime
    __to: datetime
    __min_tca_elevation: int

    def __init__(self, satellite: int = None, ground_station: int = None, from_date_time: datetime = None, to_date_time: datetime = None, min_tca_elevation: int = None):
        self.__satellite = satellite
        self.__ground_station = ground_station
        self.__from = from_date_time
        self.__to = to_date_time
        self.__min_tca_elevation = min_tca_elevation

    def to_dict(self) -> dict:
        return {
            'satellite': self.__satellite,
            'groundStation': self.__ground_station,
            'fromDateTime': self.__from,
            'toDateTime': self.__to,
            'minTcaElevation': self.__min_tca_elevation
        }
