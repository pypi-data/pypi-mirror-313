import asyncio
import time

from openi import OpenIAsyncApi


async def run_api(api: OpenIAsyncApi, order: int):
    data = await api.create_model("chenzh01/llms", model_name="sdk_create")
    print(f"requests {order} DONE\n{data}\n")
    await asyncio.sleep(1)


async def main():
    api = OpenIAsyncApi()
    print(api._shared_session)
    print(api.auth)
    print(api.base_url, "\n")

    # asynchronous calls
    tasks = [run_api(api, i) for i in range(1)]
    await asyncio.gather(*tasks)

    # synchronous calls
    # for i in range(5):
    #     await run_api(api, i)

    await api.close()


if __name__ == "__main__":
    start_time = time.time()

    # This is the main entry point of the program
    asyncio.run(main())

    print(f"took {time.time() - start_time:.4f} seconds to run.")
