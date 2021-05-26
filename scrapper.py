from datetime import datetime
import json
from abc import ABC, abstractmethod
from typing import Dict, Tuple
from bs4 import BeautifulSoup


import requests
from PIL import Image

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

class Scrapper(ABC):
    name = None

    @abstractmethod
    def get(self) -> Tuple:
        pass

    def identify(self):
        print(self.name)

    @staticmethod
    def _get_image_from_url(url: str) -> Image:
        return Image.open(requests.get(url, stream=True).raw)


class RedditScrapper(Scrapper):
    name = 'Reddit Scrapper'

    @staticmethod
    def __get_random_meme() -> Dict:
        url = 'https://meme-api.herokuapp.com/gimme'
        return requests.get(url).json()

    @staticmethod
    def __get_meme_matadata(post_uid: str) -> Dict:
        url = f'https://reddit.com/{post_uid}/.json'
        response = requests.get(url, headers={'User-agent': 'Meta Meme Scrapper'}).json()
        return response[0]['data']['children'][0]['data']

    def get(self) -> Tuple:
        random_meme = RedditScrapper.__get_random_meme()
        post_uid = random_meme['postLink'].split('/')[-1]
        metadata = RedditScrapper.__get_meme_matadata(post_uid)

        curated_metadata = {
            'source': f'r/{metadata["subreddit"]}',
            'title': metadata['title'],
            'text': metadata['selftext'],
            'created': str(datetime.fromtimestamp(metadata['created'])),
            'scrapped_at': str(datetime.now()),
            'like': metadata['ups'],
            'dislike': metadata['downs'],
            'like_ratio': metadata['ups'] / float(metadata['ups'] + metadata['downs']),
            'dislike_ratio': metadata['downs'] / float(metadata['ups'] + metadata['downs']),
            'picture_url': metadata['url_overridden_by_dest'],
            'author': metadata['author'],
            'comment_count': metadata['num_comments']
        }

        image = Scrapper._get_image_from_url(metadata['url_overridden_by_dest'])

        return curated_metadata, image


class NineGAGScrapper(Scrapper):
    name = '9GAG Scrapper'

    @staticmethod
    def __get_random_meme() -> BeautifulSoup:
        url = 'https://9gag.com/shuffle'

        options = Options()
        # options.headless = True
        # options.add_argument("--window-size=1920,1200")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        # options.add_argument("--disable-blink-features=AutomationControlled")
        #
        # driver = webdriver.Chrome(options=options)
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        el_str = driver.find_elements_by_class_name('main-wrap')[0].get_attribute('innerHTML')
        # driver.save_screenshot('screenshot.png')
        driver.quit()

        soup = BeautifulSoup(el_str, 'html.parser')

        return soup

    @staticmethod
    def __get_meme_matadata(post_uid: str) -> Dict:
        url = f'https://reddit.com/{post_uid}/.json'
        response = requests.get(url, headers={'User-agent': 'Meta Meme Scrapper'}).json()
        return response[0]['data']['children'][0]['data']

    def get(self) -> Tuple:
        rms = self.__get_random_meme() # rms -> random meme soup

        section = rms.find('a', {'class': 'section'}).contents[0]

        curated_metadata = {
            'source': f'9GAG:{section}',
            'title': None,
            'text': None,
            'created': None,
            'scrapped_at': None,
            'like': None,
            'dislike': None,
            'like_ratio': None,
            'dislike_ratio': None,
            'picture_url': None,
            'author': None,
            'comment_count': None
        }

        return curated_metadata, None
