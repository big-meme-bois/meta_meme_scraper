from datetime import datetime
import json
from abc import ABC, abstractmethod
from pprint import pprint
from typing import Dict, Tuple
from bs4 import BeautifulSoup

import requests
from PIL import Image

from selenium import webdriver
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

    def __init__(self):
        self.__initialize_driver()

    def __initialize_driver(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def __del__(self):
        self.driver.quit()

    def __get_random_meme(self) -> BeautifulSoup:
        url = 'https://9gag.com/shuffle'

        success = False
        while not success:
            try:
                self.driver.get(url)
                success = True
                break
            except Exception:
                self.__initialize_driver()

        el_str = self.driver.find_elements_by_class_name('main-wrap')[0].get_attribute('innerHTML')

        soup = BeautifulSoup(el_str, 'html.parser')

        return soup

    def get(self) -> Tuple:
        while True:
            rms = self.__get_random_meme()  # rms -> random meme soup

            section = rms.find('a', {'class': 'section'}).contents[0]
            title = rms.find('header').findChild('h1').contents[0]

            post_meta = rms.find('p', {'class': 'post-meta'}).findChildren()
            likes = post_meta[0].contents[0].replace(',', '').replace(' points', '')
            comments = post_meta[1].contents[0].replace(',', '').replace(' comments', '')

            post_tags = rms.find('div', {'class': 'post-tag'})
            text = None

            if post_tags:
                text = ' '.join(['#' + tag.contents[0] for tag in post_tags.findChildren()])

            image_post_div = rms.find('div', {'class': 'image-post'})

            if image_post_div:
                picture_url = image_post_div.findChild('img').attrs['src']

                curated_metadata = {
                    'source': f'9GAG:{section}',
                    'title': title,
                    'text': text,
                    'created': None,
                    'scrapped_at': str(datetime.now()),
                    'like': likes,
                    'dislike': None,
                    'like_ratio': None,
                    'dislike_ratio': None,
                    'picture_url': picture_url,
                    'author': None,
                    'comment_count': comments
                }

                img = self._get_image_from_url(picture_url)

                return curated_metadata, img
