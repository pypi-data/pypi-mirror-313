from typing import Any


def request_execution(python_bytecode: bytes, function_name: str) -> Any:
    ...

def load_privileged_plugin(plugin_path: str) -> None:
    ...

def invoke_method(object, method_name: str, *args) -> Any:
    ...
