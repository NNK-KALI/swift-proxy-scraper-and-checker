from src.scraper.swift_scraper import Scraper
from src.checker.threadedproxychecker import  ThreadedProxyChecker
from src.checker.asyncproxychecker import AsyncProxyChecker 

class SwiftProxy():
    def __init__(self):
        self.scraper = Scraper()
        self.proxy_checker = AsyncProxyChecker()               

    def get(self, protocol, timeout, limit):
        proxies = self.scraper.scrape(protocol)
        valid_proxies_que = self.proxy_checker.runner(proxies, _timeout=timeout, limit=limit)
        valid_proxies = []
        while not valid_proxies_que.empty():
            valid_proxies.append(valid_proxies_que.get())
        return valid_proxies


