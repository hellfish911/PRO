import asyncio

async def coroutine_simple(id):
    print(f"[coroutine_simple] start {id}")
    return f"result_{id}"

async def coroutine_with_future_manual():
    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    loop.call_soon(fut.set_result, "manual_future_done")
    result = await fut
    print(f"[coroutine_with_future_manual] got {result}")
    return result

def blocking_cpu_work():
    return sum(i * i for i in range(1000000))

async def coroutine_with_future_executor():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, blocking_cpu_work)
    print(f"[coroutine_with_future_executor] computed {result}")
    return result

async def coroutine_chained():
    task = asyncio.ensure_future(coroutine_simple(1))
    res = await task
    print(f"[coroutine_chained] got {res}")
    return res

async def coroutine_aggregator():
    results = await asyncio.gather(
        coroutine_with_future_manual(),
        coroutine_with_future_executor(),
        coroutine_simple(2)
    )
    print(f"[coroutine_aggregator] aggregated {results}")
    return results

async def coroutine_combiner():
    r1 = await coroutine_simple(3)
    r2 = await coroutine_chained()
    print(f"[coroutine_combiner] combined {r1} + {r2}")
    return r1, r2

async def main():
    tasks = [
        asyncio.create_task(coroutine_simple(0)),
        asyncio.create_task(coroutine_with_future_manual()),
        asyncio.create_task(coroutine_with_future_executor()),
        asyncio.create_task(coroutine_chained()),
        asyncio.create_task(coroutine_aggregator()),
        asyncio.create_task(coroutine_combiner()),
    ]
    all_results = await asyncio.gather(*tasks)
    print(f"[main] all results: {all_results}")

if __name__ == '__main__':
    asyncio.run(main())
