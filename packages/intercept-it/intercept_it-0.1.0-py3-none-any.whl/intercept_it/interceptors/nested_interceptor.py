from typing import Callable, Any

from intercept_it.utils.checker import arguments_checker

from intercept_it.interceptors.base_interceptor import BaseInterceptor
from intercept_it.interceptors.unit_interceptor import UnitInterceptor
from intercept_it.interceptors.global_interceptor import GlobalInterceptor
from intercept_it.interceptors.looped_interceptor import LoopedInterceptor


class NestedInterceptor:
    """ Container object for few interceptors. Routes any calls to them """
    def __init__(
            self,
            interceptors: dict[
                int | str | type[BaseException],
                UnitInterceptor | GlobalInterceptor | LoopedInterceptor
            ]
    ):
        """
        :param interceptors: The collection of specified interceptors objects
        """
        arguments_checker.check_nested_interceptors(interceptors, BaseInterceptor)
        self.interceptors = interceptors

    def intercept(self, group_id: int | str | type[BaseException]) -> Any:
        def outer(function):
            arguments_checker.check_group_existence(group_id, self.interceptors)
            interceptor = self.interceptors.get(group_id)

            if isinstance(interceptor, UnitInterceptor):
                if interceptor.async_mode:
                    async def async_wrapper():
                        return await interceptor.intercept(group_id)(function)
                    return async_wrapper
                
                return interceptor.intercept(group_id)(function)
            else:
                if interceptor.async_mode:
                    async def async_wrapper():
                        return await interceptor.intercept(function)
                    return async_wrapper
                    
                return interceptor.intercept(function)
        return outer

    def wrap(self, function: Callable, group_id: int | str | type[BaseException], *args, **kwargs) -> Any:
        arguments_checker.check_group_existence(group_id, self.interceptors)
        interceptor = self.interceptors.get(group_id)

        if isinstance(interceptor, UnitInterceptor):
            if interceptor.async_mode:
                async def async_wrapper():
                    return await interceptor.wrap(function, group_id, *args, **kwargs)
                return async_wrapper

            return interceptor.wrap(function, group_id, *args, **kwargs)
        else:
            if interceptor.async_mode:
                async def async_wrapper():
                    return await interceptor.wrap(function, *args, **kwargs)
                return async_wrapper

            return interceptor.wrap(function, *args, **kwargs)
