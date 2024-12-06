from typing import Any, Callable

loads: Callable[[str], Any]
try:
    import orjson

    loads = orjson.loads
except ImportError:
    try:
        import ujson

        loads = ujson.loads
    except ImportError:
        import json

        loads = json.loads


def json_loads(text: str) -> Any:
    return loads(text)
