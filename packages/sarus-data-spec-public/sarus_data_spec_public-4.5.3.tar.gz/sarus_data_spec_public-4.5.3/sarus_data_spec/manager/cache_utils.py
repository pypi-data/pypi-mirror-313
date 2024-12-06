import functools
import inspect
import logging
import typing as t

from cachetools import LRUCache
import pandas as pd

from sarus_data_spec.manager.typing import Computation, Manager
from sarus_data_spec.typing import Referrable

logger = logging.getLogger(__name__)


def retrieve_or_validate_cache(
    category: str, args: t.Tuple, kwargs: t.Dict
) -> t.Optional[LRUCache]:
    """
    Retrieves the cache for the specified category from the manager of the
    global context.

    Args:
        category (str): The category name for which the cache needs to be
        retrieved.

    Returns:
        LRUCache: The cache object associated with the given category.

    Raises:
        ValueError: If the category is not initialized in the cache manager.
        TypeError: If the retrieved cache is not an instance of LRUCache.
        NotImplementedError: If the global context manager's caches method
        is not implemented.
    """
    manager = get_manager_from_all_arguments(args, kwargs)

    try:
        caches = manager.caches()
    except NotImplementedError:
        return None

    if category not in caches:
        raise ValueError(
            f"""Category:{category} not initialized in the caching of
            the manager."""
        )

    cache = caches[category]
    if not isinstance(cache, LRUCache):
        raise TypeError(
            f"The cache for category '{category}' is not an LRUCache instance"
        )

    return cache


def get_manager_from_all_arguments(args: t.Tuple, kwargs: t.Dict) -> Manager:
    """Return one manager of at least one argument, otherwise
    return an error.
    """
    for arg in args:
        manager = get_manager_from_arg(arg)
        if manager is not None:
            return manager
    for _, v in kwargs.items():
        manager = get_manager_from_arg(v)
        if manager is not None:
            return manager

    raise ValueError("Impossible to retrieve a manager from the argument.")


def get_manager_from_arg(argument: t.Any) -> t.Optional[Manager]:
    """Return the manager of the argument if it exists"""
    if isinstance(argument, Referrable):
        referrable = t.cast(Referrable, argument)
        manager = referrable.manager()
        if not isinstance(manager, Manager):
            return None
        else:
            return manager
    else:
        return None


def process_argument(argument: t.Any) -> t.Any:
    """
    Processes an argument to extract a suitable representation for cache key
    construction.
    """
    if isinstance(argument, Referrable):
        referrable = t.cast(Referrable, argument)
        return referrable.uuid()
    elif isinstance(argument, Computation):
        return argument.task_name
    else:
        return argument


def build_cache_key(
    func: t.Callable, args: t.Tuple, kwargs: t.Dict, use_first_arg: bool
) -> t.Tuple:
    """
    Constructs a cache key based on the function's name and its arguments.

    Args:
        func (t.Callable): The function for which the cache key is being built.
        args (t.Tuple): The positional arguments passed to the function.
        kwargs (t.Dict): The keyword arguments passed to the function.
        use_first_arg (bool): Flag indicating whether to include the first
        argument in the key.
    """
    key: t.List[t.Any] = [func.__name__]
    start_index = 0 if use_first_arg else 1
    for arg in args[start_index:]:
        key.append(process_argument(arg))
    for k, v in kwargs.items():
        key.append((k, process_argument(v)))
    return tuple(key)


def safeguard_cache_integrity(result: t.Any) -> t.Any:
    """
    Creates a copy of the result if it's a mutable object (like a DataFrame
    or Series).
    This is to ensure that modifications to the returned object do not affect
    the cached value.
    """
    if isinstance(result, (pd.DataFrame, pd.Series)):
        return result.copy()
    return result


def lru_caching(
    category: str = "default", use_first_arg: bool = True
) -> t.Callable:
    """
    Decorator that provides caching functionality for functions, with support
    for
    both asynchronous and synchronous functions.

    Args:
        category (str): The cache category to use.
        use_first_arg (bool): Flag to include or exclude the first argument in
        the cache key.

    Returns:
        t.Callable: A decorator that when applied to a function, enables
        caching of its results.
    """

    def decorator(func: t.Callable) -> t.Any:
        is_async = inspect.iscoroutinefunction(func)

        @functools.wraps(func)
        async def async_wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return await async_cache_logic(func, *args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            return sync_cache_logic(func, *args, **kwargs)

        async def async_cache_logic(
            func: t.Callable, *args: t.Any, **kwargs: t.Any
        ) -> t.Any:
            cache = retrieve_or_validate_cache(category, args, kwargs)
            if cache is None:
                return await func(*args, **kwargs)
            key = build_cache_key(func, args, kwargs, use_first_arg)

            # computing result
            if key in cache:
                logger.info(
                    f"Cache hit for for {func.__name__} with key: {key}"
                )
                result = cache[key]
            else:
                logger.info(
                    f"Computed and cached for {func.__name__} with key: {key}"
                )
                result = await func(*args, **kwargs)
                if result is not None:
                    cache[key] = result

            return safeguard_cache_integrity(result)

        def sync_cache_logic(
            func: t.Callable, *args: t.Any, **kwargs: t.Any
        ) -> t.Any:
            cache = retrieve_or_validate_cache(category, args, kwargs)
            if cache is None:
                return func(*args, **kwargs)
            key = build_cache_key(func, args, kwargs, use_first_arg)

            # computing result
            if key in cache:
                logger.info(
                    f"Cache hit for for {func.__name__} with key: {key}"
                )
                result = cache[key]
            else:
                logger.info(
                    f"Computed and cached for {func.__name__} with key: {key}"
                )
                result = func(*args, **kwargs)
                if result is not None:
                    cache[key] = result

            return safeguard_cache_integrity(result)

        return async_wrapper if is_async else sync_wrapper

    return decorator
