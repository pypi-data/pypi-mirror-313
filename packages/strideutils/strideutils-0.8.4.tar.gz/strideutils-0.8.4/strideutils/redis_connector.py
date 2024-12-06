"""
Redis Connector for Stride Utils

This module provides a client for interacting with all the Redis databases
used in Stride. Uses stride_config to connect to different Redis instances
(public, frontend, backend, etc.) and provides methods for common Redis operations
like get, set, and scan.
"""

from typing import Dict, List, Optional, Union, cast

from redis import Redis

from strideutils.stride_config import (
    config,
    get_env_or_raise,
    get_redis_password_env_var,
)


class RedisClient:
    """Redis client to connect to multiple databases"""

    def __init__(self, db_name_or_names: Optional[Union[List[str], str]] = None) -> None:
        """
        Initializes Redis database connections.

        Args:
            db_name_or_names: Optional database name or list of database names to initialize.
                          If None, initializes all configured databases.

        Raises:
            ValueError: If db_name_or_names is an empty list or contains invalid database names.
        """
        self._dbs: Dict[str, Redis] = {}

        # Convert single name to list
        db_names = [db_name_or_names] if isinstance(db_name_or_names, str) else db_name_or_names
        # If no names specified, use all configured databases
        db_names = db_names or list(config.redis.keys())

        if not db_names:
            raise ValueError("No database names provided and no databases configured")

        # Validate database names
        invalid_db_names = [name for name in db_names if name not in config.redis]
        if invalid_db_names:
            raise ValueError(f"Invalid Redis database names: {invalid_db_names}")

        for name in db_names:
            self._dbs[name] = self._init_db(name)

    @staticmethod
    def _init_db(database_name: str) -> Redis:
        """
        Initializes a database connection.

        Args:
            database_name: Name of the database to initialize.

        Returns:
            Redis: Initialized Redis client.

        Raises:
            ValueError: If database configuration is not found.
        """
        if database_name not in config.redis:
            raise ValueError(f"Configuration not found for database: {database_name}")

        redis_config = config.redis[database_name]
        password_env = get_redis_password_env_var(database_name)
        password = get_env_or_raise(password_env)

        return Redis(
            host=redis_config.host,
            port=redis_config.port,
            password=password,
            ssl=redis_config.ssl,
            decode_responses=True,
        )

    def get_db(self, name: Optional[str] = None) -> Redis:
        """
        Returns the Redis db specified by name.
        If name is None, returns the only configured database or raises an error if multiple are configured.

        Args:
            name: Optional name of the database to retrieve.

        Returns:
            Redis: The requested Redis database client.

        Raises:
            ValueError: If no name is provided and multiple databases are configured,
                      or if the requested database name has not been configured.
        """
        if name is None:
            if len(self._dbs) != 1:
                raise ValueError("Database name must be specified if multiple databases are configured")
            return next(iter(self._dbs.values()))

        if name not in self._dbs:
            raise ValueError(f"Database {name} has not been configured.")
        return self._dbs[name]

    def get(self, key: str, db_name: Optional[str] = None) -> Optional[str]:
        """
        Reads the given Redis key and returns the value.

        Args:
            key: The key to retrieve.
            db_name: Optional name of the database to use.

        Returns:
            Optional[str]: The value associated with the key, or None if the key doesn't exist.
        """
        db = self.get_db(db_name)
        result = db.get(key)
        return cast(Optional[str], result)

    def get_multiple_keys(self, keys: List[str], db_name: Optional[str] = None) -> List[Optional[str]]:
        """
        Reads multiple keys at once.

        Args:
            keys: List of keys to retrieve.
            db_name: Optional name of the database to use.

        Returns:
            List[Optional[str]]: List of values associated with the keys.
        """
        db = self.get_db(db_name)
        results = db.mget(keys)
        return cast(List[Optional[str]], results)

    def get_all_keys(self, db_name: Optional[str] = None) -> List[str]:
        """
        Returns all keys in the specified Redis db.

        Args:
            db_name: Optional name of the database to use.

        Returns:
            List[str]: List of all keys in the database.
        """
        db = self.get_db(db_name)
        return [key for key in db.scan_iter()]

    def set(self, key: str, val: str, db_name: Optional[str] = None) -> None:
        """
        Sets the given key to value in the specified Redis db.

        Args:
            key: The key to set.
            val: The value to set.
            db_name: Optional name of the database to use.
        """
        db = self.get_db(db_name)
        db.set(key, val)

    def set_keys(self, dict_to_upload: Dict[str, str], db_name: Optional[str] = None, prefix: str = '') -> None:
        """
        Sets multiple keys and values in the Redis db.

        Args:
            dict_to_upload: Dictionary of key-value pairs to set.
            db_name: Optional name of the database to use.
            prefix: Optional prefix to add to all keys.
        """
        db = self.get_db(db_name)
        with db.pipeline() as pipe:
            for k, v in dict_to_upload.items():
                pipe.set(prefix + k, v)
            pipe.execute()
