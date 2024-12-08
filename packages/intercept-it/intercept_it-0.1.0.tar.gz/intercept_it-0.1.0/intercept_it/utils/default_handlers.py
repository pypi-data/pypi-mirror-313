import time
import asyncio


def cooldown_handler(waiting_time_in_seconds: int) -> None:
    """
    Select time delay after exception handling. Program will sleep at the specified time

    :param waiting_time_in_seconds: Time dilation value in seconds
    """
    time.sleep(waiting_time_in_seconds)


async def async_cooldown_handler(waiting_time_in_seconds: int) -> None:
    """
    Select time delay after exception handling. Program will sleep at the specified time

    :param waiting_time_in_seconds: Time dilation value in seconds
    """
    await asyncio.sleep(waiting_time_in_seconds)
