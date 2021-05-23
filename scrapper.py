from datetime import datetime
import json
from abc import ABC, abstractmethod
from typing import Dict, Tuple

import requests
from PIL import Image


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
            'created': datetime.fromtimestamp(metadata['created']),
            'scrapped_at': datetime.now(),
            'like': metadata['ups'],
            'dislike': metadata['downs'],
            'like_ratio': metadata['ups'] / float(metadata['ups'] + metadata['downs']),
            'dislike_ratio': metadata['downs'] / float(metadata['ups'] + metadata['downs']),
            'picture_url': metadata['url_overridden_by_dest'],
            'author': metadata['author']
        }

        image = Scrapper._get_image_from_url(metadata['url_overridden_by_dest'])

        return curated_metadata, image