import logging
from datetime import datetime, timedelta
from threading import Lock

from keycloak import KeycloakOpenID

from .token import Token


class Client:
    __open_id_client: KeycloakOpenID
    __username: str
    __password: str
    __company_id: int
    __token: Token = None
    __token_expires_at: datetime = None
    __lock: Lock
    __logger: logging.Logger

    def __init__(self, open_id_client: KeycloakOpenID, username: str, password: str, company_id: int, logger: logging.Logger):
        self.__open_id_client = open_id_client
        self.__username = username
        self.__password = password
        self.__company_id = company_id
        self.__lock = Lock()
        self.__logger = logger

    def token(self) -> Token:
        with self.__lock:
            if self.__token is None or self.__token_expires_at is None or datetime.now() >= self.__token_expires_at:
                self.__logger.info("Requesting auth token")
                oauth_token = self.__open_id_client.token(username=self.__username, password=self.__password)
                self.__token_expires_at = datetime.now() + timedelta(seconds=int(oauth_token['expires_in']))
                self.__token = Token(username=self.__username, company_id=self.__company_id, access_token=oauth_token['access_token'])

            return self.__token
