from typing import List
from scrapper import Scrapper, RedditScrapper

if __name__ == '__main__':
    scrappers: List[Scrapper] = [RedditScrapper()]

    for scrapper in scrappers:
        scrapper.identify()
        meta, image = scrapper.get()
        print(meta)
        image.show()
