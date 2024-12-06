import time
import asyncio

from llmer.parallel.async_parallel import AsyncParallel
from llmer.parallel.thread_pool import ThreadPool
from llmer.parallel.multi_thread import MultiThread
from llmer.parallel.async_executor import AsyncExecutor


@ThreadPool(parallel_count=4)
def thread_pool_sample_function(x, y):
    time.sleep(1.5)
    return x*y['z']**2

@MultiThread(parallel_count=4)
def multi_thread_sample_function(x, y):
    time.sleep(1.5)
    return x*y['z']**2

@AsyncExecutor(parallel_count=4)
def async_executor_sample_function(x, y):
    time.sleep(1.5)
    return x*y['z']**2

@AsyncParallel(parallel_count=4)
async def async_parallel_sample_function(x: int, y: int) -> int:
    await asyncio.sleep(1.5)
    return x*y['z']**2


class TestLLMUParallel:
    params = [{'x': 1, 'y': {'z': 2} }, {'x': 2, 'y': {'z': 3}}, {'x': 3, 'y': {'z': 4}}, {'x': 4, 'y': {'z': 5}}, {'x': 5, 'y': {'z': 6}}, {'x': 6, 'y': {'z': 7}}]

    def test(self):
        thread_pool_start = time.time()
        results = thread_pool_sample_function(parallel_params=self.params)
        thread_pool_spend = time.time() - thread_pool_start
        assert 3 <= thread_pool_spend < 3.5, f"ThreadPool time spent: {thread_pool_spend} seconds"
        print("ThreadPool Test Successfully")
        time.sleep(1)

        multi_thread_start = time.time()
        results = multi_thread_sample_function(self.params)
        multi_thread_spend = time.time() - multi_thread_start
        assert 3 <= multi_thread_spend < 3.5, f"MultiThread time spent: {multi_thread_spend} seconds."
        print("MultiThread Test Successfully")
        time.sleep(1)


    async def async_test(self):
        async_executor_start = time.time()
        results = await async_executor_sample_function(self.params)
        async_executor_spend = time.time() - async_executor_start
        assert 3 <= async_executor_spend < 3.5, f"AsyncExecutor time spent: {async_executor_spend} seconds."
        print("AsyncExecutor Test Successfully")
        await asyncio.sleep(1)

        async_parallel_start = time.time()
        results = await async_parallel_sample_function(self.params)
        async_parallel_spend = time.time() - async_parallel_start
        assert 3 <= async_parallel_spend < 3.5, f"AsyncParallel time spent: {async_parallel_spend} seconds."
        print("AsyncParallel Test Successfully")
        await asyncio.sleep(1)



    def run_tests(self):
        self.test()
        asyncio.run(self.async_test())

TestLLMUParallel().run_tests()



