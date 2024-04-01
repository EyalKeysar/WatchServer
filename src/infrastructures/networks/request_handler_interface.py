from abc import ABC, abstractmethod


class RequestHandlerInterface(ABC):
    """
    Abstract class for request handler
    """

    @abstractmethod
    def get_request(self):
        """
        Get request from client
        :param request: request from client
        :return: None
        """
        pass

    @abstractmethod
    def send_response(self, response):
        """
        Send response to client
        :param response: response to client
        :return: None
        """
        pass