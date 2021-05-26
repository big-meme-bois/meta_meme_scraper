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


if __name__ == '__main__':
    # test_repeats(RedditScrapper(), 5)

    scrapper = NineGAGScrapper()
    scrapper.get()
