from helpers.proxyscrape import ProxyScrape
from swiftproxycheckerasync import ProxyChecker as pca
from swiftproxycheckerthreading import ProxyChecker as pct 
import asyncio
import time
import csv
import json



timeout = 5
max_workers = 100
proxies_queue = ProxyScrape().scrape(protocol=["https"])
# proxies = []
# with open("newproxy.txt", "r") as f:
#     proxies = f.read().strip().splitlines()

# proxies = ProxyScrape().scrape(protocol=["https"])

async_timings = []
threading_timings = []

# async_start_time = time.time()
# asyncio.run(pca().run_checker(proxies[:i]))
# async_end_time = time.time()

threading_start_time = time.time()
pct().checker(proxies_queue=proxies_queue, _timeout=timeout, _max_workers=_max_workers)
threading_end_time = time.time()
    
# async_time = async_end_time - async_start_time
# async_timings.append(async_time)

threading_time = threading_end_time - threading_start_time
threading_timings.append(threading_time)

# print(f"stats iteration : {i}")
print(f"Time taken by thread pool exec : {async_time}sec")
# print(f"Time taken by async aiohttp: {threading_time}sec")
print()


def save_to_csv(filename, fields, rows):
    """
    This function saves a python list into a csv file.
    
    :param str filename: The name of the file to save 
    :param list(str) fields: the headers for the file(contains the column names)
    :param list(double) rows: content from the list
    :return None
    """
    with open(filename, "w") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)


def save_to_json(filename, data):
    """
    This function converts a python list to json and saves it in a file.

    :param str filename: The Name of the file you want to save to
    :param list(double) data: A python list
    :return None
    """

    with open(filename, "w") as file:
        json.dump(data, file)

save_to_json("async_timings.json", async_timings)
save_to_json("threading_timings.json", threading_timings)
