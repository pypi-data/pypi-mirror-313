import json
import time
from datetime import datetime
from typing import Callable, Iterator, Union

from .log import setup_logger

logger = setup_logger()


def caltime(func: Callable) -> Callable:
    """
    Decorator to calculate the time of a function.

    Args:
        func (function): function to be decorated

    Returns:
        function: wrapper function
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.4f} seconds to run.")
        return result

    return wrapper


def parse_time(timestamp: Union[str, int]) -> datetime:
    """
    Parse timestamp to python datetime

    Args:
        timestamp (Union[str, int]):
            unix timestamp data, either in plaintext or integer

    Returns:
        datetime: python datetime object without timezone information
    """
    if isinstance(timestamp, int):
        return datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).replace(tzinfo=None)
    elif isinstance(timestamp, str):
        return datetime.fromisoformat(timestamp).replace(tzinfo=None)
    else:
        raise ValueError("Invalid timestamp format")


def jprint(input_dict: dict, indent: int = 4):
    """Print a dict in json format

    Args:
        input_dict (dict): dict to print
        indent (int, optional): indent level. Defaults to 4.

    Example:
        >>> jprint({"a": 1, "bb": 2, "ccc": 3})
        {
            "a": 1,
            "bb": 2,
            "ccc": 3
        }
    """
    print(json.dumps(input_dict, indent=4, ensure_ascii=False))


def aprint(input_dict: dict, colon=False):
    """
    print a dict in aligned format

    :param input_dict: dict to be printed
    :param colon: aligned colon or not
    :return: None

    e.g.
    >>> aprint({"a": 1, "bb": 2, "ccc": 3})
    a:   1
    bb:  2
    ccc: 3
    """
    max_key_length = max(len(key) for key in input_dict.keys())
    for key, value in input_dict.items():
        if not colon:
            key += ":"
            formatted_key = f"{key:{max_key_length + 1}}"
            print(f"{formatted_key} {value}")
        else:
            formatted_key = f"{key:{max_key_length}}"
            print(f"{formatted_key}: {value}")


def convert_bytes(byte):
    """
    Convert bytes to human-readable units (bytes, KB, MB, GB, TB).
    """
    units = ["bytes", "KB", "MB", "GB", "TB"]
    index = 0

    while byte >= 1024 and index < len(units) - 1:
        byte /= 1024.0
        index += 1

    return f"{byte:.2f} {units[index]}"


def iter_by_step(start: int, total: int, step: int = 2) -> Iterator[list]:
    """
    A for loop that iterate {step} items each time

    Examples:
    >>> for chunks in iter_by_step(10, 3):
    >>>    print(chunks)
    [0, 1, 2]
    [3, 4, 5]
    [6, 7, 8]
    [9]
    """
    if any([start < 0, total < 0, step < 0]):
        raise ValueError("`start`, `total`, `step` should be positive integers")

    if max(start, step, total) != total:
        raise ValueError("`start` or `step` should be less than `total`")

    parts = [part for part in range(start, total)]
    for i_start in range(0, len(parts), step):
        chunks = parts[i_start : i_start + step]
        yield chunks
