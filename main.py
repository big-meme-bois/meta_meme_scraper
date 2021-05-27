from pprint import pprint

from scrapper import Scrapper, RedditScrapper, NineGAGScrapper
import imagehash


def test_repeats(scrapper: Scrapper, target_count=100):
    hash_list = []

    print('Fetching memes:')
    for i in range(target_count):
        meta, image = scrapper.get()
        img_hash = imagehash.average_hash(image)
        hash_list.append(img_hash)
        print(f'\t{i + 1}/{target_count} - {img_hash}')

    meme_count = len(hash_list)
    uniq_meme_count = len(set(hash_list))
    print()
    print(f'Fetching done! Fetched {meme_count} memes, of which {uniq_meme_count} seemed unique!')


def test_scrapper_results(scrapper: Scrapper):
    result = scrapper.get()
    pprint(result[0])
    result[1].show()


def test_scrapper_multi_results(scrapper: Scrapper, number: int):
    results = scrapper.get_multiple(number)

    for result in results:
        pprint(result[0])
        result[1].show()


if __name__ == '__main__':
    # test_scrapper_results(NineGAGScrapper())
    test_scrapper_multi_results(NineGAGScrapper(), 5)
    # test_repeats(NineGAGScrapper(), 100)
