import json
import logging
from http.client import HTTPException
from typing import List

import requests

from gridgs.sdk.auth import Client as AuthClient
from gridgs.sdk.entity import Session, session_from_dict, PredictParams


class Client:
    __base_url: str
    __auth_client: AuthClient
    __logger: logging.Logger

    def __init__(self, base_url: str, auth_client: AuthClient, logger: logging.Logger):
        self.__base_url = base_url
        self.__auth_client = auth_client
        self.__logger = logger

    def get_predicted_sessions(self, params: PredictParams) -> List[Session]:
        token = self.__auth_client.token()
        response = requests.get(self.__base_url + '/sessions/predict', params=params.to_dict(), headers={
            'Authorization': 'Bearer ' + token.access_token
        })

        sessions = []
        if response.status_code == 200:
            for row in response.json():
                sessions.append(session_from_dict(row))

        return sessions

    def create_session(self, session: Session) -> Session:
        token = self.__auth_client.token()
        create_params = {
            'satellite': {'id': session.satellite.id},
            'groundStation': {'id': session.ground_station.id},
            'startDateTime': session.start_datetime.isoformat(sep='T', timespec='auto'),
            'endDateTime': session.end_datetime.isoformat(sep='T', timespec='auto'),
        }
        response = requests.post(self.__base_url + '/sessions', data=json.dumps(create_params), headers={
            'Content-type': 'application/json', 'Authorization': 'Bearer ' + token.access_token
        })

        if response.status_code == 201:
            return session_from_dict(response.json())

        raise HTTPException('Can not create session', response.reason, response.json())
