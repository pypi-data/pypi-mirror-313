from abc import ABC, abstractmethod


class BaseLogger(ABC):
    """ Logger interface """
    @staticmethod
    @abstractmethod
    def save_logs(message: str) -> None:
        pass


class BaseAsyncLogger(BaseLogger):
    """ Async logger interface """
    @staticmethod
    async def save_logs(message: str) -> None:
        pass
