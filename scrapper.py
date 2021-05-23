from abc import ABC, abstractmethod
from typing import Dict

import requests
import PIL


class Scrapper(ABC):
    name = None

    @abstractmethod
    def get(self) -> Dict:
        pass

    def present(self):
        print(self.name)


class RedditScrapper(Scrapper):

    def __init__(self):
        self.name = 'Reddit Scrapper'

    def get(self) -> Dict:
        print(self.name)
        return {}
