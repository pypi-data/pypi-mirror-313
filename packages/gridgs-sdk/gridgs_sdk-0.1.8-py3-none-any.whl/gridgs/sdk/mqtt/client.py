import json
import logging
import uuid
from typing import Callable

from paho.mqtt.client import Client as PahoMqttClient, MQTTMessageInfo, MQTTMessage, MQTT_ERR_SUCCESS, error_string

from gridgs.sdk.auth import Client as AuthClient
from gridgs.sdk.entity import Frame, frame_from_dict, Session
from gridgs.sdk.logger_fields import with_frame, with_session, with_frame_payload_size
from .exceptions.session_not_found_exception import SessionNotFoundException
from .interface import Connector, Sender, Receiver


class Client(Connector, Sender, Receiver):
    __host: str
    __port: int
    __auth_client: AuthClient
    __mqtt_client: PahoMqttClient
    __session: Session | None = None
    __logger: logging.Logger

    def __init__(self, host: str, port: int, auth_client: AuthClient, logger: logging.Logger):
        self.__host = host
        self.__port = port
        self.__auth_client = auth_client
        self.__mqtt_client = PahoMqttClient(client_id='api-frames-' + str(uuid.uuid4()), reconnect_on_failure=True)
        self.__logger = logger

    def on_downlink(self, on_downlink: Callable[[Frame], None]):
        def on_message(client, userdata, msg: MQTTMessage):
            try:
                frame_dict = json.loads(msg.payload)
                frame = frame_from_dict(frame_dict)
                self.__logger.info('Downlink frame', extra=with_frame(frame))
                on_downlink(frame)
            except Exception as e:
                self.__logger.error(f'Error processing downlink: {e}', exc_info=True, extra={'frame_payload': msg.payload})

        self.__mqtt_client.on_message = on_message

    def connect(self, session: Session):
        self.__logger.info('Connecting', extra=with_session(session))
        self.__session = session

        def on_connect(client: PahoMqttClient, userdata, flags, reason_code):
            self.__logger.info('Connected. Subscribing', extra=with_session(session))
            client.subscribe(topic=_build_downlink_topic(session))

        self.__mqtt_client.on_connect = on_connect

        def on_disconnect(client, userdata, rc):
            self.__logger.info(f'Disconnected: {error_string(rc)}', extra=with_session(session))
            if rc != MQTT_ERR_SUCCESS:
                self.__set_credentials()

        self.__mqtt_client.on_disconnect = on_disconnect

        self.__set_credentials()
        self.__mqtt_client.connect(self.__host, self.__port)
        self.__mqtt_client.loop_forever(retry_first_connection=True)

    def disconnect(self):
        self.__logger.info('Disconnecting...', extra=with_session(self.__session))
        self.__session = None
        self.__mqtt_client.disconnect()

    def send(self, raw_data: bytes) -> MQTTMessageInfo:
        self.__logger.info('Sending uplink', extra=with_frame_payload_size(raw_data) | with_session(self.__session))
        if isinstance(self.__session, Session):
            return self.__mqtt_client.publish(topic=_build_uplink_topic(self.__session), payload=raw_data)
        raise SessionNotFoundException("Session not found. Connect first")

    def __set_credentials(self):
        token = self.__auth_client.token()
        self.__mqtt_client.username_pw_set(username=token.username, password=token.access_token)


def _build_downlink_topic(session: Session) -> str:
    return f'satellite/{session.satellite.id}/downlink/gs/{session.ground_station.id}'


def _build_uplink_topic(session: Session) -> str:
    return f'satellite/{session.satellite.id}/uplink/gs/{session.ground_station.id}'
