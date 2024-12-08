import sys
import pytz

from datetime import datetime
from loguru import logger
from typing import Callable

from intercept_it.utils.enums import WarningLevelsEnum
from intercept_it.utils.exceptions import InterceptItSetupException
from intercept_it.utils.default_formatters import std_formatter
from intercept_it.loggers.base_logger import BaseLogger


class STDLogger(BaseLogger):
    """ Implements printing logs to the console. Logger uses `loguru <https://pypi.org/project/loguru/>`_ module """
    def __init__(
            self,
            logging_level: str = WarningLevelsEnum.ERROR.value,
            pytz_timezone: str = 'Europe/Moscow',
            default_formatter: Callable = std_formatter
    ):
        """
        Supported logging levels:

        * INFO
        * WARNING
        * ERROR

        Supported timezones: `list of timezones <https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568>`_

        Message formatter is a callable, which must receives the string and returns the formatted string

        :param logging_level: One of the supported logging levels
        :param pytz_timezone: Timezone in string representation
        :param default_formatter: Message text formatter
        """
        self._logger = logger
        self._logging_level = logging_level
        self._default_timezone = pytz_timezone
        self._message_formatter = default_formatter

        self._check_logging_level()

        self._logger.configure(
            handlers=[
                {
                    'sink': sys.stdout,
                    'format': '{extra[datetime]} | {level} | {message}',
                },
            ],
            patcher=self._patch_timezone
        )

    def save_logs(self, message: str) -> None:
        """ Prints logs to console according to logging level """
        message = self._message_formatter(message)
        match self._logging_level:
            case WarningLevelsEnum.INFO.value:
                self._logger.info(message)
            case WarningLevelsEnum.ERROR.value:
                self._logger.error(message)
            case WarningLevelsEnum.WARNING.value:
                self._logger.warning(message)

    def _patch_timezone(self, record):
        """ Loguru default timezone patcher  """
        record['extra']['datetime'] = datetime.now(tz=pytz.timezone(self._default_timezone))

    def _check_logging_level(self) -> None:
        """ Checks if invalid logging level received """
        if self._logging_level not in (
            WarningLevelsEnum.INFO.value,
            WarningLevelsEnum.ERROR.value,
            WarningLevelsEnum.WARNING.value
        ):
            raise InterceptItSetupException(f'Encountered unsupported logging level: {self._logging_level}')
