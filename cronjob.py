# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
import os

# Main cronjob function.
from main import cronjob, send_commits_on_review

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler(timezone='Europe/Kiev')
print(os.environ.get("LOCAL", 0))
if os.environ.get("LOCAL", 0) == 0:
    scheduler.add_job(cronjob, 'cron', day_of_week='mon-fri', hour=21, minute="0–59/15")
else:
    scheduler.add_job(send_commits_on_review, 'interval', seconds=30)

scheduler.start()
