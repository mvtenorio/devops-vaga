import pickle
import logging
import time
from threading import Thread, current_thread
from redis import Redis, BlockingConnectionPool

import config
import tasks

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("worker")


REGISTERED_TASKS = {
    "randomize_image": tasks.randomize_image,
    "sum_even_numbers": tasks.sum_even_numbers,
}

redis_conn = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    # connection_pool=BlockingConnectionPool(max_connections=config.REDIS_POOL_SIZE),
)


def _worker():
    logger.info("Started worker (name=%s)", current_thread().name)
    while True:
        _, payload = redis_conn.blpop(["tasks"])
        task = pickle.loads(payload)
        logger.info("Received task: %s", repr(task["token"]))
        initial_execution_time = time.perf_counter()
        redis_conn.set("result:" + task["token"], pickle.dumps({"status": "received"}))

        task_fn = REGISTERED_TASKS.get(task["func"])
        if task_fn is None:
            logger.warning("Unknown task: %s", task["func"])
            continue

        try:
            result = task_fn(**task["payload"])

            lead_time = time.perf_counter() - task["initial_time"]
            execution_time = time.perf_counter() - initial_execution_time
            logger.info(
                "Task %s succeeded\nLead time: %s\nExecution time: %s",
                task["token"],
                str(lead_time),
                str(execution_time),
            )
            redis_conn.set(
                "result:" + task["token"],
                pickle.dumps({"status": "finished", "result": result}),
            )
        except Exception as exc:
            logger.warning("Task %s failed: %s", task["token"], str(exc))
            import traceback

            traceback.print_exc()
            redis_conn.set(
                "result:" + task["token"],
                pickle.dumps({"status": "errored", "exc": exc}),
            )


print(f"Starting {config.WORKER_THREADS} worker threads...")
thread_pool = []
for n in range(config.WORKER_THREADS):
    t = Thread(target=_worker, name=f"worker-{n}")
    t.start()
    thread_pool.append(t)


for t in thread_pool:
    t.join()
