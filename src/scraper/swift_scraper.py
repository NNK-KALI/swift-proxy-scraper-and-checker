from src.scraper.helpers.proxyscrape import ProxyScrape
import queue


class Scraper:
    """
    A wrapper class that calls fetches proxies from various sites using helper classes.
    """

    def scrape(self, protocol=["all"]):
        proxy_scrape_queue = ProxyScrape().scrape(protocol)
        return proxy_scrape_queue


