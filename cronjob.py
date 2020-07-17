# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
import os

# Main cronjob function.
from main import cronjob, send_commits_on_review

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler(timezone='Europe/Kiev')

if os.environ.get("LOCAL", 0) == 0:
    scheduler.add_job(send_commits_on_review, 'cron', day_of_week='mon-fri', hour=15, minute="0")
else:
    scheduler.add_job(send_commits_on_review, 'interval', seconds=30)

scheduler.start()
