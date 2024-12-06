from abc import ABC, abstractmethod
import logging

from llmbench.inference.clients.request_data import Request

logger = logging.getLogger(__name__)


class Client(ABC):

    @abstractmethod
    def make_request(self, request: Request):
        pass