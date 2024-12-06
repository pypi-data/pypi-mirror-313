import json
import logging
import typing
import uuid

from paho.mqtt.client import Client as PahoMqttClient, MQTT_ERR_SUCCESS, error_string
from paho.mqtt.client import MQTTMessage

from gridgs.sdk.auth import Client as AuthClient, Token
from gridgs.sdk.logger_fields import with_session_event
from .session_event import _session_event_from_dict, SessionEvent


class Subscriber:
    __host: str
    __port: int
    __auth_client: AuthClient
    __mqtt_client: PahoMqttClient
    __logger: logging.Logger

    def __init__(self, host: str, port: int, auth_client: AuthClient, logger: logging.Logger):
        self.__host = host
        self.__port = port
        self.__auth_client = auth_client
        self.__logger = logger
        self.__mqtt_client = PahoMqttClient(client_id='api-events-' + str(uuid.uuid4()), reconnect_on_failure=True)

    def on_event(self, func: typing.Callable[[SessionEvent], None]):
        def on_message(client, userdata, msg: MQTTMessage):
            try:
                session_event_dict = json.loads(msg.payload)
                session_event = _session_event_from_dict(session_event_dict)
                self.__logger.info('Session event received', extra=with_session_event(session_event))
                func(session_event)
            except Exception as e:
                self.__logger.error(f'Error processing session event: {e}', exc_info=True, extra={'session_event_payload': msg.payload})

        self.__mqtt_client.on_message = on_message

    def run(self):
        self.__logger.info('Starting')
        token = self.__get_token_and_set_credentials()

        def on_connect(client: PahoMqttClient, userdata, flags, reason_code):
            self.__logger.info('Connected. Subscribing')
            client.subscribe(topic=_build_sessions_event_topic(token.company_id))

        self.__mqtt_client.on_connect = on_connect

        def on_disconnect(client, userdata, rc):
            self.__logger.info(f'Disconnected: {error_string(rc)}')
            if rc != MQTT_ERR_SUCCESS:
                self.__get_token_and_set_credentials()

        self.__mqtt_client.on_disconnect = on_disconnect

        self.__mqtt_client.connect(self.__host, self.__port)
        self.__mqtt_client.loop_forever(retry_first_connection=True)

    def stop(self):
        self.__logger.info('Stopping...')
        self.__mqtt_client.disconnect()

    def __get_token_and_set_credentials(self) -> Token:
        token = self.__auth_client.token()
        self.__mqtt_client.username_pw_set(username=token.username, password=token.access_token)
        return token


def _build_sessions_event_topic(company_id: int) -> str:
    return f'company/{company_id}/session_event'
