from app import db, Keyboard
from dotenv import load_dotenv
from uuid import uuid4
import praw
import os
import re

def reddit_keyboard_scraper():
    load_dotenv()
    pattern = re.compile("[$](\d+(?:\.\d{1,2})?)")
    db.session.query(Keyboard).delete()
    db.session.commit()

    reddit = praw.Reddit(
        client_id = os.getenv("CLIENT_ID"),
        client_secret = os.getenv("CLIENT_SECRET"),
        username = os.getenv("USERNAME"),
        password = os.getenv("PASSWORD"),
        user_agent = os.getenv("USER_AGENT")
    )

    subreddit = reddit.subreddit("MechGroupBuys")
    current_group_buys = [submission for submission in subreddit.new(limit=40) if submission.link_flair_text=="LIVE"]

    for submission in current_group_buys:
        try:
            title = submission.title
            title_split = title.split(" ")
            title_end_index = title_split.index("//")
            title = " ".join(title_split[1:title_end_index])

            media_id = submission.gallery_data["items"][0]["media_id"]
            img = submission.media_metadata[media_id]["p"][0]["u"].split("?")[0].replace("preview", "i")
            
            date = " ".join(title_split[title_end_index + 1:])

            origin = "https://www.reddit.com" + submission.permalink

            info = submission.comments[0].body
            info = info.replace("**", "").replace("---", "\\n")

            price = (max([float(i) for i in pattern.findall(info)]))

            unique_id = uuid4()

            data = Keyboard(unique_id, title, img, date, price, info, origin)
            db.session.add(data)
            db.session.commit()
        except:
            # error will occur if post is not in gallery form and if $ is missing from stickied comment
            print("error scraping from {}".format("https://www.reddit.com" + submission.permalink))
            continue