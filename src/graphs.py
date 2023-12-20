import matplotlib.pyplot as plt
import json


def read_from_json(filename):
    """
    Read data from json file and return it as a object.

    :param str filename: The path to the json file.
    :return: file contents
    :rtype: dict/list
    """
    with open(filename, "r") as f:
        return json.load(f)

async_timings = read_from_json("async_timings.json")
threading_timings = read_from_json("threading_timings.json")

plt.plot(async_timings, label="async time")
plt.plot(threading_timings, label="threading time")
plt.legend()

plt.ylabel("Time")
plt.xlabel("No of proxies checked")

plt.show()
