from typing import Dict, Any, List

from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from config.environment import Environment


class CacheSystemMixin:
    @staticmethod
    def set(key, value, timeout: int | None = DEFAULT_TIMEOUT, version=None):
        """Saves a value in cache. If the key already existed, it is overwritten.

        Args:
            key (str): The key. It cannot have spaces or control characters and must be less than 250 characters.
            value (picklable Python object): Value.
            timeout (int): The default from the configuration, if not specified is 300 seconds. None saves it forever.
            version (int): The version of the saved value. To avoid deleting useful data after a code change that
                uses cached values.
        """
        Environment.logger.debug(f"Save value in cache of {key}.")
        cache.set(key, value, timeout, version)

    @staticmethod
    def get(key: str, default: Any = None, version: int = None) -> object | None:
        """Gets a cache value. If it does not exist, returns ``default`` or None if not specified."""
        Environment.logger.debug(f"Get cache value of {key}.")
        return cache.get(key, default, version)

    @staticmethod
    def add(key: str, value: Any, timeout: int = DEFAULT_TIMEOUT, version: int = None) -> bool:
        """Saves only if the key does not already exist.

        Returns:
            True if the value has been stored; False otherwise.
        """
        Environment.logger.debug(f"Save (if not exists) value in cache of {key}.")
        exists = cache.add(key, value, timeout, version)
        Environment.logger.debug(f"Saved value in cache of {key}: {exists}.")
        return exists

    @staticmethod
    def get_or_set(key: str, default: Any = None, version: int = None):
        """Get key value or save a value if it does not exist."""
        Environment.logger.debug(f"Get (or save) value in cache of {key}.")
        return cache.get_or_set(key, default, version)

    @staticmethod
    def get_many(keys: List[str], version: int = None):
        """Get multiple values from multiple keys at once."""
        Environment.logger.debug(f"Get cache values of {keys}.")
        return cache.get_many(keys, version)

    @staticmethod
    def set_many(key_values: Dict[str, Any], timeout: int = DEFAULT_TIMEOUT):
        """Cache multiple values at once."""
        Environment.logger.debug(f"Save cache values of {key_values.keys()}.")
        cache.set_many(key_values, timeout)

    @staticmethod
    def delete(key: str, version: int = None) -> bool:
        """Deletes a specific key.

        Returns:
            True if the key has been deleted successfully; False otherwise.
        """
        Environment.logger.info(f"Delete cache value of {key}.")
        delete_ok = cache.delete(key, version)
        if not delete_ok:
            Environment.logger.warning(f"Problem deleting key {key}")
        return delete_ok

    @staticmethod
    def delete_many(keys: List[str], version: int = None):
        """Deletes a list of keys.

        Returns:
            True if the keys have been deleted successfully; False otherwise.
        """
        Environment.logger.info(f"Delete cache values of {keys}.")
        cache.delete_many(keys, version)

    @staticmethod
    def clear():
        """Deletes ALL keys from the cache."""
        Environment.logger.warning("Delete ALL keys from the cache.")
        cache.clear()

    @staticmethod
    def reset_timeout(key: str, timeout: int = DEFAULT_TIMEOUT, version: int = None) -> bool:
        """Resets the expiration timeout of a key.

        Returns:
            True if the timeout has been set correctly; False otherwise
        """
        Environment.logger.debug(f"Reset timeout of {key} to {timeout} seconds.")
        timeout_ok = cache.touch(key, timeout, version)
        if not timeout_ok:
            Environment.logger.warning(f"Problem setting new timeout of {key}")
        return timeout_ok
