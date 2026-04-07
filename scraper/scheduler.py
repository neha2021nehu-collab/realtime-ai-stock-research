import asyncio
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import time
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timezone
from news_scraper import scrape_finviz_news
from deduplicator import filter_new
from storage import save_to_json

# scheduler = BlockingScheduler(timezone="UTC")
scheduler = BackgroundScheduler(timezone="UTC")

def run_scraper():
    print(f"\n[scheduler] Job triggered at {datetime.now(timezone.utc).isoformat()}")

    #APScheduler is sync, so we run the async scraper inside asyncio.run()
    news = asyncio.run(scrape_finviz_news())

    if not news:
        print("[scheduler] No headlines fetched.")
        return
    new_news = filter_new(news)

    if not new_news:
        print("[scheduler] No new headlines - skipping save.")
        return
    save_to_json(new_news)
    print(f"[scheduler] Done. {len(new_news)} headlines saved.")

@scheduler.scheduled_job(IntervalTrigger(minutes=60))
def scheduled_scrape():
    run_scraper()

if __name__=="__main__":
    print("[scheduler] Starting - first run immediately, then every 60 minutes")
    print("[scheduler] Press Ctrl+C to stop.\n")

    run_scraper()
    scheduler.start() #run immediately on startup, don't wait 60 mins

    try:
        while True:
            time.sleep(1) #keeps main thread alive
    except (KeyboardInterrupt, SystemExit):
        print("\n[scheduler] Stopping...")
        scheduler.shutdown(wait=False) #force immediate shutdown
        print("\n[scheduler] Stopped.")