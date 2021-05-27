import praw
import imagehash
from PIL import Image
import requests
from datetime import datetime

reddit = praw.Reddit(
    client_id="hIcBbGcEmuy88w",
    client_secret="SAcHN6-RGnWKaHzxx2ZYaUlM1iVWWA",
    user_agent="my user agent",
)

tags = ['memes', 'meme','trump']


def fetch_memes(quantity):
    unique_memes = []
    unique_memes_hashes = []
    for tag in tags:
        try:
            for submission in reddit.subreddit(tag).hot(limit=quantity):
                append_dictionary(unique_memes, submission, unique_memes_hashes)
            for submission in reddit.subreddit(tag).new(limit=quantity):
                append_dictionary(unique_memes, submission, unique_memes_hashes)
            for submission in reddit.subreddit(tag).controversial(limit=quantity):
                append_dictionary(unique_memes, submission, unique_memes_hashes)
            for submission in reddit.subreddit(tag).rising(limit=quantity):
                append_dictionary(unique_memes, submission, unique_memes_hashes)
            for submission in reddit.subreddit(tag).top(limit=quantity):
                append_dictionary(unique_memes, submission, unique_memes_hashes)
        except:
            print("Submission errror")
    return unique_memes


def append_dictionary(unique_memes, submission, unique_memes_hashes):
    try:
        if hash(submission) not in unique_memes_hashes and submission.url.endswith(".jpg"):
            unique_memes.append({
                'url': submission.url,
                'name': submission.name,
                'title': submission.title,
                'timestamp': datetime.fromtimestamp(submission.created_utc),
                'score': submission.score,
                'upvote_ratio': submission.upvote_ratio,
                'phash': str(imagehash.phash(get_image_from_url(submission.url)))
            })
            unique_memes_hashes.append(hash(submission))
    except:
        print("Error occured")


def get_image_from_url(url: str) -> Image:
    return Image.open(requests.get(url, stream=True).raw)


meme_dict = fetch_memes(1000)
print(f"Found {len(meme_dict)} unique memes")
print(meme_dict[77])

