from typing import Callable, Any

from intercept_it.interceptors.base_interceptor import BaseInterceptor
from intercept_it.loggers.base_logger import BaseLogger, BaseAsyncLogger
from intercept_it.utils.checker import arguments_checker


class GlobalInterceptor(BaseInterceptor):
    """ Intercepts specified exceptions from a function """

    def __init__(
            self,
            exceptions: list[type[BaseException]],
            loggers: list[BaseLogger | BaseAsyncLogger] | None = None,
            raise_exception: bool = False,
            greed_mode: bool = False,
            async_mode: bool = False,
            fast_handlers_execution: bool = True,
            fast_loggers_execution: bool = True
    ):
        """
        :param exceptions: Collection of target exceptions

        :param loggers: Collection of loggers

        :param raise_exception: If equals ``True`` interceptor sends all caught exceptions higher up the call stack.
            If not specified, feature disabled

        :param greed_mode: If equals ``True`` interceptor sends wrapped function parameters
            to some handlers. If not specified, feature disabled

        :param async_mode: If equals ``True`` interceptor can work with coroutines.
            If not specified, can wrap only ordinary functions.
            Interceptor can't wrap ordinary function and coroutine at the same time!

        :param fast_handlers_execution: If equals ``True`` handlers will be executed as tasks.
         If equals ``False`` they will be executed in order with ``await`` instruction.

        :param fast_loggers_execution: If equals ``True`` loggers will be executed as tasks.
         If equals ``False`` they will be executed in order with ``await`` instruction.
        """
        super().__init__(
            exceptions=exceptions,
            loggers=loggers,
            raise_exception=raise_exception,
            greed_mode=greed_mode,
            async_mode=async_mode,
            fast_handlers_execution=fast_handlers_execution,
            fast_loggers_execution=fast_loggers_execution
        )
        self._exceptions = exceptions
        self._raise_exception = raise_exception
        self.async_mode = async_mode

    def intercept(self, function: Callable) -> Any:
        """
        Exceptions handler of the ``GlobalInterceptor`` object. Can be used as a decorator without parentheses

        Usage example::

        @global_interceptor.intercept
        def dangerous_function(number: int, accuracy=0.1) -> float:
        """
        if self.async_mode:
            async def wrapper(*args, **kwargs):
                return await self._async_wrapper(function, args, kwargs)
        else:
            def wrapper(*args, **kwargs):
                return self._sync_wrapper(function, args, kwargs)
        return wrapper

    def wrap(self, function: Callable, *args, **kwargs) -> Any:
        """
        Exceptions handler of the ``GlobalInterceptor`` object. Can be used as a function with parameters

        Usage example::

        global_interceptor.wrap(dangerous_function, 5, accuracy=0.3)

        :param function: Wrapped function
        :param args: Positional arguments of the function
        :param kwargs: Keyword arguments of the function
        """
        arguments_checker.check_function(function)
        if self.async_mode:
            async def wrapper():
                return await self._async_wrapper(function, args, kwargs)
            return wrapper()
        else:
            return self._sync_wrapper(function, args, kwargs)

    def _sync_wrapper(self, function: Callable, args, kwargs) -> Any:
        """
        Executes the main control logic of the wrapped function

        :param function: Wrapped function
        :param args: Positional arguments of the function
        :param kwargs: Keyword arguments of the function
        """
        try:
            return function(*args, **kwargs)
        except BaseException as exception:
            if exception.__class__ not in self._exceptions:
                raise exception

            self._execute_sync_handlers(exception, *args, **kwargs)

            if self._raise_exception:
                raise exception

    async def _async_wrapper(self, function: Callable, args, kwargs) -> Any:
        """
        Executes the main control logic of the wrapped coroutine

        :param function: Wrapped function
        :param args: Positional arguments of the function
        :param kwargs: Keyword arguments of the function
        """
        try:
            return await function(*args, **kwargs)
        except BaseException as exception:
            if exception.__class__ not in self._exceptions:
                raise exception

            await self._execute_async_handlers(exception, *args, **kwargs)

            if self._raise_exception:
                raise exception
