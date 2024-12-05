import configparser
import typing

from diamond_shovel.function.task import WorkerPool, TaskContext


class Event:
    ...

class DiamondShovelInitEvent(Event):
    config: configparser.ConfigParser
    daemon: bool
    ...

class WorkerPoolInitEvent(Event):
    pool: WorkerPool
    ...

class WorkerEvent(Event):
    plugin_name: str
    worker_name: str
    ...

class WorkerFinishEvent(WorkerEvent):
    error: Exception
    ...

class TaskEvent(Event):
    task_context: TaskContext
    ...

class TaskDispatchEvent(TaskEvent):
    ...

class TaskReadTriggerEvent(TaskEvent):
    key: str
    value: typing.Any

class TaskWriteTriggerEvent(TaskEvent):
    key: str
    value: typing.Any
    old_value: typing.Any

def register_event(init_ctx, evt_class, handler):
    ...

def call_event(evt):
    ...
