import asyncio
import random
import time

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def data_producer(future: asyncio.Future, data_id: int):
    print(f"{Colors.OKCYAN}[Producer {data_id}]: Starting data production...{Colors.ENDC}")
    for _ in range(random.randint(3, 6)):
        await asyncio.sleep(0)
    result_data = f"Data Packet-{data_id}-{random.randint(100, 999)}"
    print(f"{Colors.OKGREEN}[Producer {data_id}]: Data '{result_data}' is ready.{Colors.ENDC}")
    future.set_result(result_data)

async def data_consumer(future: asyncio.Future, consumer_id: int):
    print(f"{Colors.WARNING}[Consumer {consumer_id}]: Waiting for data...{Colors.ENDC}")
    produced_data = await future
    print(f"{Colors.OKBLUE}[Consumer {consumer_id}]: Successfully consumed '{produced_data}'.{Colors.ENDC}")

async def independent_worker(worker_id: int):
    print(f"[Worker {worker_id}]: Starting my independent task.")
    task_duration = random.randint(2, 5)
    for i in range(task_duration):
        print(f"[Worker {worker_id}]: Progress {i+1}/{task_duration}...")
        await asyncio.sleep(0)
    print(f"[Worker {worker_id}]: Finished my task.")

async def main():
    print(f"{Colors.HEADER}--- Asynchronous Execution ---{Colors.ENDC}")
    start_time = time.time()

    loop = asyncio.get_running_loop()

    future1 = loop.create_future()
    future2 = loop.create_future()

    tasks = [
        data_producer(future1, 1),
        data_consumer(future1, 1),
        data_producer(future2, 2),
        data_consumer(future2, 2),
        independent_worker(101),
        independent_worker(102),
        independent_worker(103),
    ]

    await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"\n{Colors.HEADER}--- All tasks completed in {end_time - start_time:.4f} seconds ---{Colors.ENDC}")

if __name__ == "__main__":
    asyncio.run(main())