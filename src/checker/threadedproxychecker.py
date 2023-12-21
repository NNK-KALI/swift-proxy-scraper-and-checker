import threading
import queue
import concurrent.futures
import requests

class ThreadedProxyChecker:
    def __init__(self):
        """
        constructor for ProxyChecker class.
        """
        pass 

    def checker(self, proxies_queue, _timeout=5, _max_workers=100, limit=5):
        """
        This function takes a list of proxies and checks them concurrently using ThreadPoolExecutor.
        Currently checks only http and https.

        :param queue proxies_queue: A queue containing proxies (FIFO).
        :param int _timeout: Timeout for the request.
        :param int _max_workers: maximum no of workers for ThreadPoolExecutor.
        :param int limit: No of working proxies to return.
        :return valid_proxies_queue: A queue containing working proxies (FIFO).
        :rtype queue
        """
        valid_proxies_queue = queue.Queue()
       
        def check_proxy(valid_proxies_queue, proxy, _timeout, limit):
            try:
                response = requests.get(
                    "https://ipinfo.io/json", proxies={"http": proxy, "https": proxy}, timeout=_timeout
                )
                if response.status_code == 200:
                    if valid_proxies_queue.qsize() < limit:
                        valid_proxies_queue.put(proxy)
                        print(f"[proxychecker] [Threaded] Valid proxy found: {proxy}")
                    else:
                        # print("shuting down")
                        self.executor.shutdown(wait=False, cancel_futures=True)
            except Exception as e:
                # print(f"[proxychecker] [Threaded] Error {e}")
                pass
        futures = []
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=_max_workers)
        while not proxies_queue.empty() and valid_proxies_queue.qsize() < limit:
            proxy = proxies_queue.get()
            futures.append(self.executor.submit(check_proxy, valid_proxies_queue, proxy, _timeout, limit))
        self.executor.shutdown(wait=True)
        return valid_proxies_queue

