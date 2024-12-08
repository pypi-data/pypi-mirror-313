from typing import Callable, Any

from intercept_it.interceptors.base_interceptor import BaseInterceptor
from intercept_it.loggers.base_logger import BaseLogger, BaseAsyncLogger
from intercept_it.utils.checker import arguments_checker


class UnitInterceptor(BaseInterceptor):
    """ Intercepts specified exception from a function """
    def __init__(
            self,
            loggers: list[BaseLogger | BaseAsyncLogger] | None = None,
            raise_exception: bool = False,
            greed_mode: bool = False,
            async_mode: bool = False,
            fast_handlers_execution: bool = True,
            fast_loggers_execution: bool = True
    ):
        """
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
            loggers=loggers,
            raise_exception=raise_exception,
            greed_mode=greed_mode,
            async_mode=async_mode,
            fast_handlers_execution=fast_handlers_execution,
            fast_loggers_execution=fast_loggers_execution
        )
        self._raise_exception = raise_exception
        self.async_mode = async_mode

    def intercept(self, exception: type[BaseException]) -> Any:
        """
        Exceptions handler of the ``UnitInterceptor`` object. Can be used with specified ``Exception``

        Usage example::

        @unit_interceptor.intercept(ValueError)
        def dangerous_function(number: int, accuracy=0.1) -> float:

        :param exception: Target exception
        """
        def outer(function):
            arguments_checker.check_exceptions([exception])
            if self.async_mode:
                async def wrapper(*args, **kwargs):
                    return await self._async_wrapper(function, exception, args, kwargs)
            else:
                def wrapper(*args, **kwargs):
                    return self._sync_wrapper(function, exception, args, kwargs)
            return wrapper
        return outer

    def wrap(self, function: Callable, exception: type[BaseException], *args, **kwargs) -> Any:
        """
        Exceptions handler of the ``GlobalInterceptor`` object. Can be used as a function with parameters

        Usage example::

        unit_interceptor.wrap(dangerous_function, ValueError, 5, accuracy=0.3)

        :param function: Wrapped function
        :param exception: Target exception
        :param args: Positional arguments of the function
        :param kwargs: Keyword arguments of the function
        """
        arguments_checker.check_function(function)
        arguments_checker.check_exceptions([exception])
        if self.async_mode:
            async def wrapper():
                return await self._async_wrapper(function, exception, args, kwargs)
            return wrapper()
        else:
            return self._sync_wrapper(function, exception, args, kwargs)

    def _sync_wrapper(self, function: Callable, target_exception: type[BaseException], args, kwargs) -> Any:
        """
        Executes the main control logic of the wrapped function

        :param function: Wrapped function
        :param target_exception: Target exception
        :param args: Positional arguments of the function
        :param kwargs: Keyword arguments of the function
        """
        try:
            return function(*args, **kwargs)
        except BaseException as exception:
            if exception.__class__ != target_exception:
                raise exception

            self._execute_sync_handlers(exception, *args, **kwargs)

            if self._raise_exception:
                raise exception

    async def _async_wrapper(self, function: Callable, target_exception: type[BaseException], args, kwargs) -> Any:
        """
        Executes the main control logic of the wrapped coroutine

        :param function: Wrapped function
        :param args: Positional arguments of the function
        :param kwargs: Keyword arguments of the function
        """
        try:
            return await function(*args, **kwargs)
        except BaseException as exception:
            if exception.__class__ != target_exception:
                raise exception

            await self._execute_async_handlers(exception, *args, **kwargs)

            if self._raise_exception:
                raise exception
