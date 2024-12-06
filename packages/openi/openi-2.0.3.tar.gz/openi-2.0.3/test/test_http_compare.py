# httpx 库替换 requests，发送网络请求，原生支持异步、同步两种模式
# asyncio 标准库，执行异步代码
# concurrent.futures 标准库，执行多线程代码

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

from _auth import (
    access_token,
    endpoint
)


def get_user():
    with httpx.Client() as client:
        resp = client.get(
            endpoint,
            headers={"Authorization": f"token {access_token}"},
        )
        resp.raise_for_status()

        time.sleep(1)
        return resp.json()


def basic_run(total: int):
    start_time = time.time()

    data = []
    for i in range(total):
        data.append(get_user())

        # print(f"basic_run {i} DONE\n")

    print(f"basic_run() {data[-1]}")
    print(f"basic_run() len data[] {len(data)}")
    print(f"basic_run() took {time.time() - start_time:.4f} seconds to run.")


def threadpool_run(total: int):
    start_time = time.time()

    data = []
    with ThreadPoolExecutor(total) as executor:
        for i in range(total):
            future = executor.submit(get_user)
            data.append(future.result())
            # print(f"threadpool {i} DONE\n")

    print(f"threadpool_run() {data[-1]}")
    print(f"async_main() len data[] {len(data)}")
    print(f"threadpool_run() took {time.time() - start_time:.4f} seconds to run.")


async def async_get_user():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            endpoint,
            headers={"Authorization": f"token {access_token}"},
        )
        resp.raise_for_status()

        await asyncio.sleep(1)
        return resp.json()


async def async_main(total):
    start_time = time.time()

    # asynchronous calls
    tasks = [async_get_user() for i in range(total)]
    data = await asyncio.gather(*tasks)

    print(f"async_main() {data[-1]}")
    print(f"async_main() len data[] {len(data)}")
    print(f"async_main() took {time.time() - start_time:.4f} seconds to run.")

    # synchronous calls
    # for i in range(5):
    #     await run_api(api, i)


if __name__ == "__main__":
    total = 64

    # This is the main entry point of the program
    asyncio.run(async_main(total))

    threadpool_run(total)

    basic_run(total)
