# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import cronjob

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler(timezone='Europe/Kiev')
scheduler.add_job(cronjob, 'cron', day_of_week='mon-fri', hour=21, minute=50)

scheduler.start()
