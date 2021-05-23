from typing import List
from scrapper import Scrapper, RedditScrapper

if __name__ == '__main__':
    scrappers: List[Scrapper] = [RedditScrapper()]

    for scrapper in scrappers:
        scrapper.get()
        scrapper.present()
