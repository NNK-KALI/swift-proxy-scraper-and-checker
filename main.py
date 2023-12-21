from src.scraper.swift_scraper import Scraper
from src.checker.threadedproxychecker import  ThreadedProxyChecker
from src.checker.asyncproxychecker import AsyncProxyChecker 
import asyncio


proxies = Scraper().scrape(protocol=["https"])
print(f"scraped proxies queue len : {proxies.qsize()}")
tpc = ThreadedProxyChecker()
apc = AsyncProxyChecker()
async_working_proxies = apc.runner(proxies, _timeout=5, limit=60)
print(f"[async] working proxies queue len : {async_working_proxies.qsize()}")
# threaded_working_proxies = tpc.checker(proxies, _timeout=1, _max_workers=100,  limit=100)
# print(f"[threaded] working proxies queue len : {threaded_working_proxies.qsize()}")


