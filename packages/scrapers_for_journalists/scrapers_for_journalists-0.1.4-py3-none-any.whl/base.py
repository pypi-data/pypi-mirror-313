import re
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup


class BaseScraper:
    """
    A generic class with generic usuable functions for scraping
    """

    def __init__(self):
        self.starting_time = time.time()

    def time_from_start(self):
        return "--- %s seconds ---" % (time.time() - self.starting_time)

    def get(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        return BeautifulSoup(response.text, features="html.parser")

    def extract(self, pattern, text: str, slicing: Optional[slice] = None) -> str:
        result = dict(enumerate(re.findall(pattern, text)))

        if 1 in result.keys():
            if slicing is not None:
                return list(result.values())[slicing]
            else:
                return " & ".join(result.values())
        else:
            return result.get(0, None)
