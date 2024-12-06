import uuid
from datetime import datetime

from .ground_station import GroundStation, ground_station_from_dict
from .horizontal_coords import HorizontalCoords, horizontal_coords_to_dict, horizontal_coords_from_dict
from .satellite import Satellite, satellite_from_dict


class Session:
    _id: uuid.UUID
    _satellite: Satellite
    _ground_station: GroundStation
    _start_datetime: datetime
    _end_datetime: datetime
    _status: str
    _tca_coords: HorizontalCoords
    _created_by: str

    STATUS_SCHEDULED = 'scheduled'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'

    def __init__(self, id: uuid.UUID, satellite: Satellite, ground_station: GroundStation, start_datetime: datetime, end_datetime: datetime, status: str, tca_coords: HorizontalCoords, created_by: str):
        self._id = id
        self._satellite = satellite
        self._ground_station = ground_station
        self._start_datetime = start_datetime
        self._end_datetime = end_datetime
        self._status = status
        self._tca_coords = tca_coords
        self._created_by = created_by

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def satellite(self) -> Satellite:
        return self._satellite

    @property
    def ground_station(self) -> GroundStation:
        return self._ground_station

    @property
    def start_datetime(self) -> datetime:
        return self._start_datetime

    @property
    def end_datetime(self) -> datetime:
        return self._end_datetime

    @property
    def status(self) -> str:
        return self._status

    def statuses(self) -> list:
        return [self.STATUS_SCHEDULED, self.STATUS_IN_PROGRESS, self.STATUS_SUCCESS, self.STATUS_FAILED]

    @property
    def tca_coords(self) -> HorizontalCoords:
        return self._tca_coords

    @property
    def created_by(self) -> str:
        return self._created_by

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'status': self.status,
            'satellite': {'id': self.satellite.id},
            'groundStation': {'id': self.ground_station.id},
            'startDateTime': self.start_datetime.isoformat(sep='T', timespec='auto'),
            'endDateTime': self.end_datetime.isoformat(sep='T', timespec='auto'),
            'tcaCoords': horizontal_coords_to_dict(self.tca_coords),
            'createdBy': self._created_by,
        }


def session_from_dict(ses: dict) -> Session:
    return Session(
        id=uuid.UUID(ses['id']),
        satellite=satellite_from_dict(ses['satellite']) if 'satellite' in ses else None,
        ground_station=ground_station_from_dict(ses['groundStation']) if 'groundStation' in ses else None,
        status=ses['status'] if 'status' in ses else None,
        start_datetime=datetime.fromisoformat(ses['startDateTime']) if 'startDateTime' in ses else None,
        end_datetime=datetime.fromisoformat(ses['endDateTime']) if 'endDateTime' in ses else None,
        tca_coords=horizontal_coords_from_dict(ses['tcaCoords']) if 'tcaCoords' in ses else None,
        created_by=ses['createdBy'] if 'createdBy' in ses else None,
    )
