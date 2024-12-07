from __future__ import annotations

import asyncio
import datetime
import os
import struct
import typing
from itertools import chain

from loguru import logger
from redis.asyncio import (
    ConnectionPool as AsyncConnectionPool,
    SSLConnection as AsyncSSLConnection,
)
from redis.asyncio import Redis as AsyncRedisBase
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from redis.retry import Retry

from good_common.dependencies import BaseProvider
from redis import ConnectionPool, StrictRedis, SSLConnection

_Key = typing.Union[str, bytes, int, float]
_Value = typing.Union[str, bytes, int, float, bool, None]


_script_psadd = """
local _target_key = KEYS[1]
local _name = ARGV[1]
local _value = ARGV[2]
local _score = ARGV[3]

local hash_table = _name .. ':t'
local sorted_set = _name .. ':s'
local exclusion_set = _name .. ':exc'
local expiration_set = _name .. ':exp'
                                
redis.call('SADD', ':ps:keys', _name)
                                
if redis.call('SISMEMBER', exclusion_set, _target_key) == 0 and redis.call('ZSCORE', expiration_set, _target_key) == false then
    redis.call('HSET', hash_table, _target_key, _value)
    return tonumber(redis.call('ZINCRBY', sorted_set, _score, _target_key))
else
    return tonumber(0)
end
"""

_script_pspull = """
local _name = ARGV[1]
local _count = ARGV[2]
local _purge = ARGV[3]
local _gate = ARGV[4]
local _expire_in = ARGV[5] or 1

local sorted_set = _name .. ':s'
local expiration_set = _name .. ':exp'
local hash_table = _name .. ':t'
local exclusion_set = _name .. ':exc'

local output = {}
for i = 1, tonumber(_count) do
    local result = redis.call('ZPOPMAX', sorted_set, 1)
    if next(result) == nil then break end
    local key = result[1]
    local value = redis.call('HGET', hash_table, key)
    if value then
        table.insert(output, key)
        table.insert(output, value)

        if _purge == '1' then
            redis.call('HDEL', hash_table, key)
            if _gate == '1' then
                redis.call('SADD', exclusion_set, key)
            end
        else
            redis.call('ZADD', sorted_set, -1, key)
        end

        redis.call('ZADD', expiration_set, _expire_in, key)
        
    end
end

return output
"""

_script_psdecrementall = """
local _name = ARGV[1]
local _decrement = ARGV[2]

local sorted_set = _name .. ':s'

local keys = redis.call('ZRANGE', sorted_set, 0, -1)

for i, key in ipairs(keys) do
    redis.call('ZINCRBY', sorted_set, -_decrement, key)
end

return 1
"""


class Redis(StrictRedis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__psadd = self.register_script(_script_psadd)
        self.__pspull = self.register_script(_script_pspull)
        self.__psdecrementall = self.register_script(_script_psdecrementall)

    #
    # Prioritized Stream
    #
    def psadd(
        self, name: str, key: _Key, value: _Value, score: int = 1, readd: bool = False
    ):
        if readd:
            self.srem(f"{name}:exc", key)
            self.zrem(f"{name}:exp", key)

        return self.__psadd(keys=[key], args=[name, value, score])

    def psaddmany(
        self, name: str, items: list[tuple[_Key, _Value, int]], readd: bool = False
    ):
        pipe = self.pipeline()

        if readd:
            pipe.srem(f"{name}:exc", *[key for key, _, _ in items])
            pipe.zrem(f"{name}:exp", *[key for key, _, _ in items])

        for key, value, score in items:
            self.__psadd(keys=[key], args=[name, value, score], client=pipe)

        return pipe.execute()

    def pspull(
        self,
        name: str,
        count: int = 1,
        purge: bool = True,
        gate: bool = False,
        expire_at: datetime.timedelta | datetime.datetime = datetime.timedelta(
            minutes=24 * 60
        ),
    ):
        """
        args:
        name: str - name of the prioritized stream
        count: int - number of items to pull
        purge: bool - remove the item from the stream
        gate: bool - add the item to the exclusion set
        expire_at: datetime.timedelta | datetime.datetime - time to expire the item


        """

        if isinstance(expire_at, datetime.timedelta):
            expire_at = datetime.datetime.now(tz=datetime.UTC) + expire_at

        r = self.__pspull(
            args=[
                name,
                count,
                "1" if purge else "0",
                "1" if gate else "0",
                int(expire_at.timestamp()),
            ]
        )

        _result = {r[i]: r[i + 1] for i in range(0, len(r), 2)}

        return {
            key.decode("utf-8") if isinstance(key, bytes) else key: _result[key]
            for key in _result
        }

    def pskeys(self, name: str, **kwargs):
        return self.zrange(f"{name}:s", 0, -1, **kwargs)

    def psvalues(self, name: str):
        v = self.hgetall(f"{name}:t")
        return {
            key.decode("utf-8") if isinstance(key, bytes) else key: value
            for key, value in v.items()
        }

    def psdelete(self, name: str):
        self.delete(f"{name}:t", f"{name}:s", f"{name}:exc", f"{name}:exp")
        self.srem(":ps:keys", name)

    def psincrement(self, name: str, key: _Key, score: int):
        return self.zincrby(f"{name}:s", score, key)

    def psdeletebelowthreshold(self, name: str, threshold: int, gate: bool = False):
        keys = self.zrangebyscore(f"{name}:s", "-inf", threshold)
        pipe = self.pipeline()
        for key in keys:
            pipe.hdel(f"{name}:t", key)
            pipe.zrem(f"{name}:s", key)
            if gate:
                pipe.sadd(f"{name}:exc", key)
        pipe.execute()
        return keys

    def pslen(self, name: str):
        return self.zcard(f"{name}:s")

    def psget(self, name: str, key: _Key):
        return self.hget(f"{name}:t", key)

    def psdecrement_all(self, name: str, decrement: int):
        return self.__psdecrementall(args=[name, decrement])

    def psexpire(self):
        ts = int(datetime.datetime.now().timestamp())
        for key in self.smembers(":ps:keys"):
            key = key.decode("utf-8")
            expired_keys = self.zrangebyscore(f"{key}:exp", "-inf", ts)
            for ekey in expired_keys:
                self.zrem(f"{key}:exp", ekey.decode("utf-8"))
                self.hdel(f"{key}:t", ekey.decode("utf-8"))
                self.zrem(f"{key}:s", ekey.decode("utf-8"))

    def _hashany(self, value: typing.Any):
        return struct.pack(">Q", hash(value) & 0xFFFFFFFFFFFFFFFF)

    def hashset_add(self, collection, value: typing.Any):
        self.sadd(collection, self._hashany(value))

    def hashset_remove(self, collection, value: typing.Any):
        self.srem(collection, self._hashany(value))

    def hashset_contains(self, collection, value: typing.Any):
        return self.sismember(collection, self._hashany(value)) == 1

    def hashset_clear(self, collection):
        self.delete(collection)


class RedisProvider(BaseProvider[Redis], Redis):
    instance_cache: dict[tuple[typing.Any, ...], Redis] = {}

    def initializer(self, cls_args, cls_kwargs, fn_kwargs):
        return cls_args, cls_kwargs

    @classmethod
    def provide(cls, *args, **kwargs):
        _key = tuple(chain.from_iterable([args, kwargs.items()]))
        # logger.info(f'Key: {_key}')
        if _key not in cls.instance_cache:
            # logger.info("Creating new Redis instance")
            retry = Retry(ExponentialBackoff(), 3)
            connection_args: dict[str, typing.Any] = dict(
                host=kwargs.get("host", os.environ.get("REDIS_HOST", "localhost")),
                port=kwargs.get("port", int(os.environ.get("REDIS_PORT", "6379"))),
                db=kwargs.get("db", int(os.environ.get("REDIS_DB", "0"))),
                decode_responses=kwargs.get("decode_responses", False),
                protocol=3,
                retry=retry,
                retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
            )
            if username := kwargs.get("username", os.environ.get("REDIS_USERNAME")):
                connection_args["username"] = username

            if password := kwargs.get("password", os.environ.get("REDIS_PASSWORD")):
                connection_args["password"] = password

            if use_ssl := kwargs.get("use_ssl", os.environ.get("REDIS_USE_SSL")):
                if isinstance(use_ssl, str):
                    if use_ssl.upper() in ("TRUE", "1"):
                        connection_args["connection_class"] = SSLConnection
                elif isinstance(use_ssl, bool) and use_ssl is True:
                    connection_args["connection_class"] = SSLConnection

            connection_pool = ConnectionPool(**connection_args)
            cls.instance_cache[_key] = super().provide(connection_pool=connection_pool)
        return cls.instance_cache[_key]


class AsyncRedis(AsyncRedisBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__psadd = self.register_script(_script_psadd)
        self.__pspull = self.register_script(_script_pspull)
        self.__psdecrementall = self.register_script(_script_psdecrementall)

    async def psadd(
        self,
        name: str,
        key: _Key,
        value: _Value,
        score: int = 1,
        readd: bool = False,
        with_decay: bool = False,
    ):
        async with self.pipeline() as pipe:
            if readd:
                await pipe.srem(f"{name}:exc", key)
                await pipe.zrem(f"{name}:exp", key)

            if with_decay:
                await pipe.sadd(":ps:decay", name)

            await self.__psadd(keys=[key], args=[name, value, score], client=pipe)
            r = await pipe.execute()
            if readd:
                return r[-1]
            else:
                return r

    async def psaddmany(
        self,
        name: str,
        items: list[tuple[_Key, _Value, int]],
        readd: bool = False,
        with_decay: bool = False,
    ):
        async with self.pipeline() as pipe:
            if readd:
                pipe.srem(f"{name}:exc", *[key for key, _, _ in items])
                pipe.zrem(f"{name}:exp", *[key for key, _, _ in items])

            if with_decay:
                await pipe.sadd(":ps:decay", name)

            for key, value, score in items:
                await self.__psadd(keys=[key], args=[name, value, score], client=pipe)

            r = await pipe.execute()
            if readd:
                return r[2:]
            else:
                return r

    async def pspull(
        self,
        name: str,
        count: int = 1,
        purge: bool = True,
        gate: bool = False,
        expire_at: datetime.timedelta | datetime.datetime = datetime.timedelta(
            minutes=24 * 60
        ),
    ):
        if isinstance(expire_at, datetime.timedelta):
            expire_at = datetime.datetime.now(tz=datetime.UTC) + expire_at

        r = await self.__pspull(
            args=[
                name,
                count,
                "1" if purge else "0",
                "1" if gate else "0",
                int(expire_at.timestamp()),
            ]
        )

        _result = {r[i]: r[i + 1] for i in range(0, len(r), 2)}

        return {
            key.decode("utf-8") if isinstance(key, bytes) else key: _result[key]
            for key in _result
        }

    async def pskeys(self, name: str, **kwargs):
        return await self.zrange(f"{name}:s", 0, -1, **kwargs)

    async def psnames(self):
        return await self.smembers(":ps:keys")

    async def psdecay(self):
        return await self.smembers(":ps:decay")

    async def psvalues(self, name: str):
        v = await self.hgetall(f"{name}:t")
        return {
            key.decode("utf-8") if isinstance(key, bytes) else key: value
            for key, value in v.items()
        }

    async def psdelete(self, name: str):
        print(name)
        async with self.pipeline() as pipe:
            await pipe.delete(f"{name}:t", f"{name}:s", f"{name}:exc", f"{name}:exp")
            await pipe.srem(":ps:keys", name)
            return await pipe.execute()

    async def psincrement(self, name: str, key: _Key, score: int):
        return await self.zincrby(f"{name}:s", score, key)

    async def psdeletebelowthreshold(
        self, name: str, threshold: int, gate: bool = False
    ):
        async with self.pipeline() as pipe:
            keys = await self.zrangebyscore(f"{name}:s", "-inf", threshold)
            for key in keys:
                await pipe.hdel(f"{name}:t", key)
                await pipe.zrem(f"{name}:s", key)
                if gate:
                    await pipe.sadd(f"{name}:exc", key)
            await pipe.execute()
            return keys

    async def pslen(self, name: str):
        return await self.zcard(f"{name}:s")

    async def psget(self, name: str, key: _Key):
        return await self.hget(f"{name}:t", key)

    async def psdecrement_all(self, name: str, decrement: int):
        return await self.__psdecrementall(args=[name, decrement])

    async def psexpire(self):
        ts = int(datetime.datetime.now().timestamp())
        async with self.pipeline() as pipe:
            # logger.info(ts)
            for key in await self.smembers(":ps:keys"):
                key = key.decode("utf-8")
                # logger.info((f'{key}:exp', '-inf', ts))
                expired_keys = await self.zrangebyscore(f"{key}:exp", "-inf", ts)
                # logger.info(expired_keys)
                for ekey in expired_keys:
                    await self.zrem(f"{key}:exp", ekey.decode("utf-8"))
                    await self.hdel(f"{key}:t", ekey.decode("utf-8"))
                    await self.zrem(f"{key}:s", ekey.decode("utf-8"))

            return await pipe.execute()

    def _hashany(self, value: typing.Any):
        return struct.pack(">Q", hash(value) & 0xFFFFFFFFFFFFFFFF)

    async def hashset_add(self, collection, *values: typing.Any):
        if len(values) == 0:
            return
        _values = [self._hashany(value) for value in values]
        return await self.sadd(collection, *_values)

    async def hashset_remove(self, collection, value: typing.Any):
        return await self.srem(collection, self._hashany(value))

    async def hashset_contains(self, collection, value: typing.Any):
        return (await self.sismember(collection, self._hashany(value))) == 1

    async def hashset_clear(self, collection):
        return await self.delete(collection)


class AsyncRedisClient:
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    async def __aenter__(self) -> AsyncRedis:
        self.redis = AsyncRedis(connection_pool=self.pool)
        return self.redis

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.redis.close()


class AsyncRedisProvider(BaseProvider[AsyncRedis], AsyncRedis):
    instance_cache: dict[tuple[typing.Any, ...], AsyncRedis] = {}

    def initializer(self, cls_args, cls_kwargs, fn_kwargs):
        return cls_args, cls_kwargs

    @classmethod
    def provide(cls, *args, **kwargs):
        _key = tuple(chain.from_iterable([args, kwargs.items()]))
        # logger.info(f'Key: {_key}')
        if _key not in cls.instance_cache:
            # logger.info("Creating new Redis instance")
            retry = Retry(ExponentialBackoff(), 3)
            connection_args: dict[str, typing.Any] = dict(
                host=kwargs.get("host", os.environ.get("REDIS_HOST", "localhost")),
                port=kwargs.get("port", int(os.environ.get("REDIS_PORT", "6379"))),
                db=kwargs.get("db", int(os.environ.get("REDIS_DB", "0"))),
                decode_responses=kwargs.get("decode_responses", False),
                protocol=3,
                retry=retry,
                retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
            )
            if username := kwargs.get("username", os.environ.get("REDIS_USERNAME")):
                connection_args["username"] = username

            if password := kwargs.get("password", os.environ.get("REDIS_PASSWORD")):
                connection_args["password"] = password

            if use_ssl := kwargs.get("use_ssl", os.environ.get("REDIS_USE_SSL")):
                if use_ssl in (True, "TRUE"):
                    connection_args["connection_class"] = AsyncSSLConnection

            connection_pool = AsyncConnectionPool(**connection_args)

            cls.instance_cache[_key] = super().provide(connection_pool=connection_pool)
        return cls.instance_cache[_key]


class AsyncRedisClientProvider(BaseProvider[AsyncRedisClient], AsyncRedisClient):
    instance_cache: dict[tuple[typing.Any, ...], AsyncConnectionPool] = {}

    def initializer(self, cls_args, cls_kwargs, fn_kwargs):
        return cls_args, cls_kwargs

    @classmethod
    def provide(cls, *args, **kwargs):
        _key = tuple(chain.from_iterable([args, kwargs.items()]))
        if _key not in cls.instance_cache:
            # logger.info("Creating new Redis instance")
            retry = Retry(ExponentialBackoff(), 3)

            connection_args: dict[str, typing.Any] = dict(
                host=kwargs.get("host", os.environ.get("REDIS_HOST", "localhost")),
                port=kwargs.get("port", int(os.environ.get("REDIS_PORT", "6379"))),
                db=kwargs.get("db", int(os.environ.get("REDIS_DB", "0"))),
                decode_responses=kwargs.get("decode_responses", False),
                protocol=3,
                retry=retry,
                retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
            )
            if username := kwargs.get("username", os.environ.get("REDIS_USERNAME")):
                connection_args["username"] = username

            if password := kwargs.get("password", os.environ.get("REDIS_PASSWORD")):
                connection_args["password"] = password

            if use_ssl := kwargs.get("use_ssl", os.environ.get("REDIS_USE_SSL")):
                if use_ssl in (True, "TRUE"):
                    connection_args["connection_class"] = AsyncSSLConnection

            connection_pool = AsyncConnectionPool(**connection_args)
            cls.instance_cache[_key] = connection_pool

        return AsyncRedisClient(pool=cls.instance_cache[_key])

    @classmethod
    async def close(cls):
        await asyncio.gather(*[pool.aclose() for pool in cls.instance_cache.values()])
        cls.instance_cache.clear()
        return True
