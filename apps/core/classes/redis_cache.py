import json
from typing import Any, List
import datetime as dt

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from temporis.format import TemporisFormat

from apps.core.classes.cache import Cache
from config.environment import Environment


class RedisCache(Cache):
    @staticmethod
    def hset(name, key=None, value=None, mapping=None, timeout=DEFAULT_TIMEOUT, version=None) -> int:
        """Saves a value or set of values in a dictionary in cache (a hash).

        If the ``name`` already existed, the new key-value pairs are added (or overwritten).
        The ``key`` and ``value`` parameters must be used together or only ``mapping``.
        The ``timeout`` applies to the entire hash and not to individual keys.

        Args:
            name (str): The name of the dictionary (hash).
            key (str): The key. It cannot have spaces or control characters and must be less than 250 characters.
            value (str): Value.
            mapping (dict): Dictionary of key-value pairs to be added to name.
            timeout (int): The default from the configuration, if not specified is 300 seconds. None saves it forever.
            version (int): The version of the saved value. To avoid deleting useful data after a code change that uses cached values.

        Returns:
            The number of saved values.
        """
        Environment.logger.debug(f"Save hash in cache of {name}/{key}.")
        redis_client = cache._cache.get_client()  # noqa
        # set timeout
        try:
            timeout = int(timeout)
        except (ValueError, TypeError):
            timeout = settings.CACHES["default"].get("TIMEOUT", 300)
        # set prefix
        env_prefix = settings.CACHES["default"].get("KEY_PREFIX", "TEST")
        _version = version if version is not None else 1
        _name = f"{env_prefix}:{_version}:{name}"
        # convert None to '' in mapping dict
        if mapping is None:
            mapping = {}
        _mapping = {}
        for k, v in mapping.items():
            _mapping[k] = v if v is not None else ""
        # save to Redis
        out = redis_client.hset(name=_name, key=key, value=value, mapping=_mapping)
        # set expiration timeout
        redis_client.expire(name, time=timeout)
        return out

    @staticmethod
    def hget(name: str, key: str, default: Any = None, version: int = None) -> object | None:
        """Gets a cache value. If it does not exist, returns ``default``.

        If ``"decode_responses": False`` is set in Redis settings, a binary value will be obtained even if a string was saved.
        """
        Environment.logger.debug(f"Get hash value of {name}/{key}.")
        redis_client = cache._cache.get_client()  # noqa
        # set prefix
        env_prefix = settings.CACHES["default"].get("KEY_PREFIX", "TEST")
        _version = version if version is not None else 1
        _name = f"{env_prefix}:{_version}:{name}"
        out = redis_client.hget(_name, key)
        if isinstance(out, bytes):
            out = out.decode("utf8")
        return out if out is not None else default

    @staticmethod
    def hgetall(name: str, version: int = None) -> object | None:
        """Gets all values associated with the ``name`` key."""
        Environment.logger.debug(f"Get all values of the hash {name}.")
        redis_client = cache._cache.get_client()
        # set prefix
        env_prefix = settings.CACHES["default"].get("KEY_PREFIX", "TEST")
        _version = version if version is not None else 1
        _name = f"{env_prefix}:{_version}:{name}"
        out = {}
        _out = redis_client.hgetall(_name)
        for k, v in _out.items():
            out[k.decode("utf8")] = v.decode("utf8")
        return out

    @staticmethod
    def get_json(key: str, version: int = None) -> object | None:
        """Gets the cache info of ``key`` in JSON format.

        Use if the info is stored in JSON format. If the info is in pickle, use ``.get()`` directly.
        """
        Environment.logger.debug(f"Get cache info of {key}.")
        redis_client = cache._cache.get_client()  # noqa
        # set prefix
        env_prefix = settings.CACHES["default"].get("KEY_PREFIX", "TEST")
        _version = version if version is not None else 1
        _key = f"{env_prefix}:{_version}:{key}"
        # decode data
        info = redis_client.get(_key).decode("utf8").replace("'", '"')
        # transform into JSON
        if isinstance(info, dict):
            return info
        elif isinstance(info, str):
            return json.loads(info)
        else:
            raise ValueError(f"The value of the key {key} is neither a dictionary nor a json.")

    @staticmethod
    def keys(pattern: str = "*") -> List[str]:
        """Gets the list of keys that match the ``pattern``"""
        Environment.logger.debug(f"Get cache key list of {pattern}.")
        redis_client = cache._cache.get_client()  # noqa
        keys = redis_client.keys(pattern)
        keys = [k.decode("utf8") for k in keys]
        return keys

    @staticmethod
    def delete_by_date(date: dt.date, version=None):
        """Deletes the list of keys that match the ``date``"""
        keys = RedisCache.keys(f"*{date.strftime(TemporisFormat.YEAR_MONTH_DAY)}*")
        RedisCache.delete_many(keys, version)
