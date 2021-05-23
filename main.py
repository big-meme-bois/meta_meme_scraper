from typing import List
from scrapper import Scrapper, RedditScrapper
import imagehash

if __name__ == '__main__':
    scrapper = RedditScrapper()

    hash_list = []

    target_count = 5000

    print('Fetching memes:')
    for i in range(target_count):
        meta, image = scrapper.get()
        img_hash = imagehash.average_hash(image)
        hash_list.append(img_hash)
        print(f'\t{i+1}/{target_count} - {img_hash}')

    meme_count = len(hash_list)
    uniq_meme_count = len(set(hash_list))
    print()
    print(f'Fetching done! Fetched {meme_count} memes, of which {uniq_meme_count} seemed unique!')







