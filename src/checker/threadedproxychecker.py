import requests
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class ThreadedProxyChecker:

    def __init__(self):
        """
        constructor for ProxyChecker class.
        """
        self.lock = threading.Lock() # mutex lock to avoid race conditions

    
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
                if int(response.status_code) == 200: 
                    if valid_proxies_queue.qsize() < limit:
                        valid_proxies_queue.put(proxy)
                        print(f"[proxychecker] [Threaded] found valid proxy: {proxy}")
                        return True
                    else:
                        print("raising error")
                        raise ValueError("shutdown")
            except Exception as e:
                # print(f"[proxychecker] [Threaded] Error {e}")
                pass
            return False
                
        futures = []
        with ThreadPoolExecutor(max_workers=_max_workers) as executor:
            while (not proxies_queue.empty()):
                proxy = proxies_queue.get()
                futures.append(executor.submit(check_proxy, valid_proxies_queue, proxy, _timeout, limit))
            print(len(futures))
            try:
                for future in as_completed(futures):
                    future.result()
            except Exception as e:
                print("caught value err exception", e)
                if True:
                    executor._threads.clear()
                    concurrent.futures.thread._threads_queues.clear()
        return valid_proxies_queue

