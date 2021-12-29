from apscheduler.schedulers.blocking import BlockingScheduler
from scraper import reddit_keyboard_scraper
scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=3)
def interval_job():
    reddit_keyboard_scraper()
    
scheduler.start()