import asyncio
import time
from concurrent.futures import (
    as_completed,
    ThreadPoolExecutor
)
from pathlib import Path
from typing import Iterator

import aiofiles


def create_testing_file(filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        for i in range(10):
            f.write(str(i))


async def async_read_part(filepath: Path, part_number: int):
    async with aiofiles.open(filepath, mode="r") as f:
        print(f"reading part {part_number}")
        await f.seek(part_number)
        data = await f.read(1)

    await asyncio.sleep(1)
    return data.strip()


async def async_read_all(filepath: Path):
    tasks = [async_read_part(filepath, i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    return results


def read_part(filepath: Path, part_number: int):
    with open(filepath, mode="r") as f:
        print(f"reading part {part_number}")
        f.seek(part_number)
        data = f.read(1)

    time.sleep(1)
    return data.strip()


def read_all(filepath: Path):
    results = [read_part(filepath, i) for i in range(10)]
    return results


def thread_read_all(filepath: Path):
    results = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        for chunks in iter_by_step(0, 10, 3):
            futures = [executor.submit(read_part, filepath, i) for i in chunks]
            chunks_results = [future.result() for future in as_completed(futures)]
            results.append(chunks_results)

    return results


def iter_by_step(start: int, total: int, step: int = 2) -> Iterator[list]:
    """
    A for loop that iterate {step} items each time

    Examples:
    >>> for chunks in iter_by_step(0, 10, 3):
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
    for i_start in range(start, total, step):
        chunks = parts[i_start : i_start + step]
        yield chunks


if __name__ == "__main__":
    # time elapsed
    start_time = time.time()

    """
    main start 
    """
    test_file = Path("./data/aiofiles/ten_lines_number.txt")
    if not test_file.exists():
        create_testing_file(test_file)

    # choose only one of them to run
    # numbers = asyncio.run(async_read_all(test_file))
    # numbers = read_all(test_file)
    numbers = thread_read_all(test_file)
    print(numbers)

    """
    main end
    """

    # time elapsed
    print(f"took {time.time() - start_time:.4f} seconds to run.")
