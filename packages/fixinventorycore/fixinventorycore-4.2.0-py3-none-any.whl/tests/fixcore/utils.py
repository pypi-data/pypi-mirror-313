from typing import Callable, Awaitable, Union
from datetime import timedelta
import asyncio


async def eventually(
    predicate: Callable[[], Union[bool, Awaitable[bool]]],
    timeout: timedelta = timedelta(seconds=5),
    interval: timedelta = timedelta(seconds=0.1),
) -> None:
    async def condition() -> bool:
        predicate_result = predicate()
        if isinstance(predicate_result, Awaitable):
            predicate_result = await predicate_result
        return predicate_result

    async def wait_for_condition() -> None:
        while not await condition():
            await asyncio.sleep(interval.total_seconds())

    await asyncio.wait_for(wait_for_condition(), timeout.total_seconds())
