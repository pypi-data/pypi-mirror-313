import inspect
from typing import Callable, Any

from intercept_it.utils.exceptions import InterceptItSetupException, InterceptItRunTimeException
from intercept_it.loggers.base_logger import BaseLogger


class ArgumentsChecker:
    """
    Implements additional checks of interceptor parameters. Can raise two exceptions:

    * InterceptItSetupException when interceptor receives invalid parameters during initialization
    * InterceptItRunTimeException when interceptor receives invalid parameters at runtime
    """
    def check_setup_parameters(
            self,
            loggers: list[BaseLogger] | None = None,
            exceptions: list[type[BaseException]] | None = None,
            raise_exception: bool = False,
            greed_mode: bool = False,
            async_mode: bool = False,
            fast_handlers_execution: bool = False,
            fast_loggers_execution: bool = False
    ) -> None:
        self.check_exceptions(exceptions)
        self.check_loggers(loggers)

        self.check_boolean_arguments(
            {
                'raise_exception': raise_exception,
                'greed_mode': greed_mode,
                'async_mode': async_mode,
                'fast_handlers_execution': fast_handlers_execution,
                'fast_loggers_execution': fast_loggers_execution
            }
        )

    def check_nested_interceptors(
            self,
            interceptors: dict[int | str | type[BaseException], Any],
            base_interceptor_class
    ) -> None:
        """
        Checks if group_ids and interceptors have invalid format

        :param interceptors: Interceptors collection
        :param base_interceptor_class: Parent interceptor
        """
        for key in interceptors:
            if (
                    not isinstance(key, int) and
                    not isinstance(key, str) and
                    self.check_exceptions([key])
            ):
                raise InterceptItSetupException(
                    'Wrong key type for nested interceptors. Expected int or str or type[BaseException]'
                )

        for interceptor in interceptors.values():
            if not isinstance(interceptor, base_interceptor_class):
                raise InterceptItSetupException(
                    f'Received invalid interceptor object: {interceptor.__class__}. '
                    f'Expected BaseInterceptor subclasses'
                )

    @staticmethod
    def check_exceptions(exceptions: list[type[BaseException]] | None) -> None:
        if exceptions:
            for exception in exceptions:
                try:
                    if not isinstance(exception(), BaseException):
                        raise InterceptItSetupException(
                            f'Received wrong exception object: {exception.__class__}'
                        )
                except TypeError:
                    raise InterceptItSetupException(
                        f'Received wrong exception object: {exception.__class__}'
                    )

    @staticmethod
    def check_loggers(loggers: list[BaseLogger] | None) -> None:
        """ Checks if all of received loggers are subclasses of the ``BaseLogger`` """
        if loggers:
            for logger in loggers:
                if not isinstance(logger, BaseLogger):
                    raise InterceptItSetupException(
                        f'Wrong logger subclass: {logger.__class__.__name__}. It must implements BaseLogger class'
                    )

    @staticmethod
    def check_timeout(timeout: int) -> None:
        if not isinstance(timeout, int) and not isinstance(timeout, float):
            raise InterceptItSetupException(f'Wrong type {type(timeout)} for timeout parameter. Expected int, float')

    @staticmethod
    def check_boolean_arguments(arguments: dict[str, bool]) -> None:
        for name, value in arguments.items():
            if not isinstance(value, bool):
                raise InterceptItSetupException(f'Wrong type for "{name}" parameter. Expected boolean')

    @staticmethod
    def check_function(function: Callable) -> None:
        if not function:
            raise InterceptItRunTimeException('Target function not specified')
        # TODO: Протестировать на методах класса
        if not inspect.isfunction(function):
            raise InterceptItRunTimeException(f'Received invalid function: {function}')

    @staticmethod
    def check_group_existence(
            group_id: int | str | type[BaseException],
            interceptors: dict[int | str | type[BaseException], Any]
    ) -> None:
        if not interceptors.get(group_id):
            raise InterceptItRunTimeException(f'Received invalid group_id: {group_id}')


arguments_checker = ArgumentsChecker()
