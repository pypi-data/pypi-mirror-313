import uuid

from gridgs.sdk.entity import Frame, Session, Satellite, GroundStation, SessionEvent


def with_satellite(value: Satellite) -> dict:
    if isinstance(value, Satellite):
        return {"satellite_id": value.id}
    return {}


def with_ground_station(value: GroundStation) -> dict:
    if isinstance(value, GroundStation):
        return {"ground_station_id": value.id}
    return {}


def with_session_id(id: uuid.UUID):
    if isinstance(id, uuid.UUID):
        return {"session_id": str(id)}
    return {}


def with_session(session: Session) -> dict:
    if isinstance(session, Session):
        return with_session_id(session.id) | with_satellite(session.satellite) | with_ground_station(session.ground_station) | {"session_status": session.status}
    return {}


def with_frame(frame: Frame) -> dict:
    if isinstance(frame, Frame):
        return {"frame_id": str(frame.id)} | with_session(frame.session) | with_frame_payload_size(frame.raw_data)
    return {}


def with_frame_payload_size(raw_data: bytes) -> dict:
    if isinstance(raw_data, bytes):
        return {"frame_payload_size": len(raw_data)}
    return {}


def with_session_event(value: SessionEvent) -> dict:
    if isinstance(value, SessionEvent):
        return {"event_type": value.type} | with_session(value.session)
    return {}
