import praw
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="agentscrape"
)

def reddit_crawler(subreddit_name: str, limit: int = 10):
    data_list = []
    try:
        for submission in reddit.subreddit(subreddit_name).hot(limit=limit):
            entry = {
                "title": submission.title.strip(),
                "url": submission.url.strip(),
                "selftext": submission.selftext.strip() if submission.selftext else "",
                "upvote_ratio": submission.upvote_ratio,
                "timestamp": submission.created_utc,
                "num_comments": submission.num_comments
            }
            data_list.append(entry)
    except Exception as e:
        print(f"Error fetching subreddit {subreddit_name}: {e}")
    return clean_data(data_list)

def clean_data(data_list):
    cleaned = []
    seen_titles = set()
    for entry in data_list:
        if not entry.get("title") or not entry.get("url"):
            continue
        if entry["title"] in seen_titles:
            continue
        seen_titles.add(entry["title"])
        cleaned.append(entry)
    return cleaned
