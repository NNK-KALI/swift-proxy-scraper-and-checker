import requests
import time
import queue


class ProxyScrape:

    def __init__(self):
        self.proxies_queue = queue.Queue()


    def scrape(self, protocol = ["all"], timeout = 10000, country = ["all"], ssl = "all", anonymity = ["all"]) -> list[str]:
        """
        This function makes a request to the api endpoint of the proxyscrape and gets the list of proxies.
        """
        start_time = time.time()
        protocol = ",".join(protocol) # convert list of protocols to a single string seperated by comma
        country = ",".join(country) # convert list of countries to a single string seperated by comma
        anonymity = ",".join(anonymity) # convert list of countries to a single string seperated by comma
        api_endpoint = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout={timeout}&country={country}&ssl={ssl}&anonymity={anonymity}"

        try:
            response = requests.get(api_endpoint)
            response_status_code = response.status_code
            if int(response_status_code) == 200:
                response_text = response.text
                proxies = response_text.splitlines()
                for proxy in proxies:
                    self.proxies_queue.put(proxy)
                # for proxy in proxies:
                #     print(proxy)
                end_time = time.time()
                print(f"[proxyscraper] Total time taken to scrape proxies from proxyscrape: {end_time - start_time}", "\n")
                return self.proxies_queue
            return None
        except Exception as e:
            print(e)
            return None



