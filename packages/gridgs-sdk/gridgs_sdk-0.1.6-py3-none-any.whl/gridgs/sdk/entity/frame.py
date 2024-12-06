import base64
import uuid
from datetime import datetime

from .session import Session, session_from_dict


class Frame:
    __id: uuid.UUID
    __created_at: datetime
    __session: Session
    __raw_data: bytes
    __extra_data: dict

    def __init__(self, id: uuid.UUID, created_at: datetime, session: Session, raw_data: bytes, extra_data: dict|None = None):
        self.__id = id
        self.__created_at = created_at
        self.__session = session
        self.__raw_data = raw_data
        self.__extra_data = {} if extra_data is None else extra_data

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def session(self) -> Session:
        return self.__session

    @session.setter
    def session(self, value: Session):
        self.__session = value

    @property
    def raw_data(self) -> bytes:
        return self.__raw_data

    @property
    def extra_data(self) -> dict:
        return self.__extra_data


def frame_from_dict(fr: dict) -> Frame:
    # @TODO if no session build from groundstation and sputnik
    session = session_from_dict(fr['communicationSession'])
    return Frame(
        id=uuid.UUID(fr['id']),
        created_at=datetime.fromisoformat(fr['createdAt']) if 'createdAt' in fr else None,
        session=session,
        raw_data=base64.b64decode(fr['rawData']) if 'rawData' in fr else None,
        extra_data=fr['extraData'] if 'extraData' in fr else None
    )
