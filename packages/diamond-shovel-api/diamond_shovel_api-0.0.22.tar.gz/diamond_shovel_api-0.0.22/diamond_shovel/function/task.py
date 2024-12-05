from enum import Enum
from typing import Callable, Coroutine, Any, AsyncIterator

from diamond_shovel.plugins import PluginInitContext


class TaskContext:
    async def get_worker_result(self, plugin_name, worker_name):
        ...

    async def get_remaining_workers(self) -> list[str]:
        ...

    async def get(self, item):
        ...

    async def set(self, key, value):
        ...

    def collect(self, key: str, size: int = 10) -> AsyncIterator[Any]:
        ...

    def __getitem__(self, item):
        ...

    def __setitem__(self, key, value):
        ...

    def operate(self, key, func, *args, **kwargs):
        ...


class WorkerPool:
    def register_worker(self, plugin_ctx: PluginInitContext, worker: Callable[[TaskContext], Coroutine[Any, Any, Any]], nice: int = 0):
        ...

pools: dict[str, WorkerPool] = {}
