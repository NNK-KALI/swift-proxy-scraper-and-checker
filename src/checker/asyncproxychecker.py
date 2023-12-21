import asyncio
import aiohttp
import queue
import time

class AsyncProxyChecker:
    def __init__(self):
        """
        Initializes an AsyncProxyChecker object.
        """

        self.tasks = []
        self.limit_reached = False

    def cancel_all_tasks(self):
        """
        Cancels all asynchronous tasks in the `tasks` list.
        """

        for task in self.tasks:
            task.cancel()

    async def check_proxy(self, session, proxy, valid_proxies_queue, limit):
        """
        Check a proxy to determine if it is working or not within the specified timeout.

        @param aiohttp.session session: Aiohttp session variable.
        @param str proxy: Proxy to be checked.
        @param queue.Queue valid_proxies_queue: Queue to store valid proxies.
        @param int limit: Maximum number of valid proxies to be stored.
        """

        start_time = time.time()
        try:
            async with session.get(
                "https://ipinfo.io/json", proxy=f"http://{proxy}", ssl=False
            ) as response:
                if response.status == 200 and not self.limit_reached:
                    if valid_proxies_queue.qsize() >= limit:
                        # Stop checking once the limit is reached
                        self.limit_reached = True
                        self.cancel_all_tasks()
                        return

                    valid_proxies_queue.put(proxy)
                    print(f"[proxychecker] [async] Valid proxy found: {proxy}")
        except asyncio.TimeoutError as timeout_error:
            # print(f"[proxychecker] [async] Error: Time out.")
            pass
        except Exception as err:
            # print(f"[proxychecker] [async] Error: {err} time: {time.time() - start_time}")
            pass

    async def checker(self, session, proxies, valid_proxies_queue, limit):
        """
        Asynchronously checks a list of proxies using multiple tasks.

        @param aiohttp.session session: Aiohttp session variable.
        @param list proxies: List of proxies to be checked.
        @param queue.Queue valid_proxies_queue: Queue to store valid proxies.
        @param int limit: Maximum number of valid proxies to be stored.
        """

        try:
            self.tasks = [asyncio.create_task(self.check_proxy(session, proxy, valid_proxies_queue, limit)) for proxy in proxies]
            await asyncio.gather(*self.tasks, return_exceptions=False)
        except asyncio.CancelledError:
            # Handle CancelledError gracefully
            pass
        except Exception as er:
            print(f"[proxychecker] [async] Error: {er}")

    async def run_checker(self, valid_proxies_queue, proxies_queue, _timeout=10, limit=5):
        """
        Runs the proxy checker asynchronously.

        @param queue.Queue valid_proxies_queue: Queue to store valid proxies.
        @param queue.Queue proxies_queue: Queue containing proxies to be checked.
        @param int _timeout: Timeout for the aiohttp client session.
        @param int limit: Maximum number of valid proxies to be stored.

        @return: queue.Queue: Queue containing valid proxies.
        """

        self.limit_reached = False
        timeout = aiohttp.ClientTimeout(total=_timeout)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                await self.checker(session, list(proxies_queue.queue), valid_proxies_queue, limit)
        except Exception as e:
            print(f"[proxychecker] [async] Error: {e}")
        finally:
            self.cancel_all_tasks()
        return valid_proxies_queue

    def runner(self, proxies_queue, _timeout, limit):
        """
        Runs the proxy checker synchronously.

        @param queue.Queue proxies_queue: Queue containing proxies to be checked.
        @param int _timeout: Timeout for the aiohttp client session.
        @param int limit: Maximum number of valid proxies to be stored.

        @return: queue.Queue: Queue containing valid proxies.
        """

        self.tasks = []
        self.limit_reached = False
        valid_proxies_queue = queue.Queue()
        try:
            asyncio.run(self.run_checker(valid_proxies_queue, proxies_queue, _timeout, limit))
        except Exception as error:
            print(error)
        return valid_proxies_queue
