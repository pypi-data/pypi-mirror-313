from abc import ABC, abstractmethod
from typing import Callable

from paho.mqtt.client import MQTTMessageInfo

from gridgs.sdk.entity import Frame, Session


class Connector(ABC):
    @abstractmethod
    def connect(self, session: Session) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass


class Sender(ABC):
    @abstractmethod
    def send(self, raw_data: bytes) -> MQTTMessageInfo:
        pass


class Receiver(ABC):
    def on_downlink(self, on_downlink: Callable[[Frame], None]):
        pass
