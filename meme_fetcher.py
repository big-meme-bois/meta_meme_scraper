import praw

reddit = praw.Reddit(
    client_id="hIcBbGcEmuy88w",
    client_secret="SAcHN6-RGnWKaHzxx2ZYaUlM1iVWWA",
    user_agent="my user agent",
)

tags = ['memes', 'meme','dunkmeme','topmemes']


def fetch_memes(quantity):
    unique_memes = []
    unique_memes_hashes = []
    try:
        for tag in tags:
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
        print("Error occured")
    return unique_memes


def append_dictionary(unique_memes, submission, unique_memes_hashes):
    if hash(submission) not in unique_memes_hashes and submission.url.endswith(".jpg"):
        unique_memes.append({
            'url': submission.url,
            'name': submission.name,
            'title': submission.title,
            'timestamp': submission.created_utc,
            'score': submission.score,
            'upvote_ratio': submission.upvote_ratio
        })
        unique_memes_hashes.append(hash(submission))


meme_dict = fetch_memes(1000)
print(len(meme_dict))
print(meme_dict[12])

