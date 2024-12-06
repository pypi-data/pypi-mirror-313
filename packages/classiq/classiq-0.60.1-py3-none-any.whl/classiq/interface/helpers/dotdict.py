from typing import Any


class DotDict(dict):
    def __getattr__(self, key: str) -> Any:
        return super().get(key)

    def __setattr__(self, key: str, value: Any) -> None:
        super().__setitem__(key, value)

    def __delattr__(self, key: str) -> None:
        super().__delitem__(key)


def get_recursive_dotdict(obj: Any) -> Any:
    if not isinstance(obj, dict):
        return obj
    return DotDict({k: get_recursive_dotdict(v) for k, v in obj.items()})
