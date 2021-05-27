import praw

reddit = praw.Reddit(
    client_id="hIcBbGcEmuy88w",
    client_secret="SAcHN6-RGnWKaHzxx2ZYaUlM1iVWWA",
    user_agent="my user agent",
)


def fetch_memes(quantity):
    unique_memes_url = []
    for submission in reddit.subreddit("meme").hot(limit=quantity):
        if submission.url not in unique_memes_url and submission.url.endswith(".jpg"):
            unique_memes_url.append(submission.url)
    for item in unique_memes_url:
        print(item)
    return unique_memes_url


fetch_memes(20)
