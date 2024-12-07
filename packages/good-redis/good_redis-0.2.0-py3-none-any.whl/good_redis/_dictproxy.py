import typing
from good_common.utilities import try_chain
from fast_depends import inject
from ._client import Redis, RedisProvider
from loguru import logger

_convert_value = try_chain(
    [
        lambda value: int(value),
        lambda value: float(value),
        lambda value: value.decode(),
        lambda value: value,
    ]
)


class DictProxy:
    @inject
    def __init__(
        self,
        name: str,
        expires: int = 60 * 60 * 24,
        default_object: dict | None = None,
        redis: Redis = RedisProvider(),
    ):
        self._name = name
        self._expires = expires
        self._redis = redis

        self._keys_and_defaults = default_object or {}

        for key in self.__class__.__annotations__.keys():
            self._keys_and_defaults[key] = self.__class__.__dict__[key]

        self._methods = set()

        for key in self.__class__.__dict__.keys():
            if not key.startswith("_") and isinstance(
                self.__class__.__dict__[key], property
            ):
                self._methods.add(key)

    def __getitem__(self, key):
        if key not in self._keys_and_defaults:
            raise KeyError(f"Key {key} not found in defaults")
        if (val := self._redis.hget(self._name, key)) is not None:
            return _convert_value(val)
        return self._keys_and_defaults.get(key)

    def __setitem__(self, key, value):
        # logger.debug(f"Setting {self._name}.{key} to {value}")
        self._redis.hset(self._name, key, value)
        self._redis.expire(self._name, self._expires)

    def __getattribute__(self, name: str) -> typing.Any:
        if name.startswith("_") or name in self._methods:
            return super().__getattribute__(name)
        return self[name]

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name.startswith("_"):
            return super().__setattr__(name, value)
        self[name] = value

    @property
    def __dict__(self):
        return {
            k.decode(): _convert_value(v)
            for k, v in self._redis.hgetall(self._name).items()
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._name} {self.__dict__}>"
