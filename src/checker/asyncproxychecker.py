import asyncio
import aiohttp
import queue
import time

class AsyncProxyChecker:
    def __init__(self):
        self.tasks = []
        # self.limit = 1

    def cancel_all_tasks(self):
        print("canceling task")
        for task in self.tasks:
            task.cancel()


    async def check_proxy(self, session, proxy, valid_proxies_queue, limit):
        s = time.time()
        try:
            async with session.get(
                "https://ipinfo.io/json", proxy=f"http://{proxy}", ssl=False
            ) as response:
                if response.status == 200:
                    
                    if valid_proxies_queue.qsize() >= limit:
                        # Stop checking once the limit is reached
                        self.cancel_all_tasks()
                         
                    valid_proxies_queue.put(proxy)
                    print(f"[proxychecker] [async] valid proxy found: {proxy}")

        except Exception as err:
            print(f"[proxychecker] [async] Error: {err} t: {time.time()- s}")

    async def checker(self, session, proxies, valid_proxies_queue, limit):
        try:
            tasks = [self.check_proxy(session, proxy, valid_proxies_queue, limit) for proxy in proxies]
            
            await asyncio.gather(*tasks, return_exceptions=False)
            self.tasks = tasks
        except Exception as er:
            print(f"[proxychecker] [async] Error: {er}")

    async def run_checker(self, valid_proxies_queue, proxies_queue, _timeout=10, limit=5):
        # valid_proxies_queue = queue.Queue()
        # limit = limit
        timeout = aiohttp.ClientTimeout(total=_timeout)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                await self.checker(session, list(proxies_queue.queue), valid_proxies_queue, limit)
        except Exception as e:
            print(f"[proxychecker] [async] Error: {e}" )
        return valid_proxies_queue

    def runner(self, proxies_queue, _timeout, limit):
        valid_proxies_queue = queue.Queue()
        try:
            asyncio.run(self.run_checker(valid_proxies_queue, proxies_queue, _timeout, limit))
        except Exception as error:
            print(error)
        return valid_proxies_queue

