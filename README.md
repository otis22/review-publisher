# review-publisher

![Build Status](https://github.com/otis22/review-publisher/workflows/CI/badge.svg)


Heroku app for publish commit for review

## Inspired
https://saqibameen.com/deploy-python-cron-job-scripts-on-heroku/

# Local start 
LOCAL=1 GITLAB_URL=u PRIVATE_TOKEN=k PROJECT_ID=1 PROJECT_PATH=r/p BRANCHES=master,develop SLACK_URL=u SLACK_CHANNEL=#developers python cronjob.py

#Start on heroku
1. Clone or copy repo
1. In Heroku set envs like screen https://prnt.sc/tjo398
1. Change schedule in cronjob.py in line scheduler.add_job(send_commits_on_review, 'cron', day_of_week='mon-fri', hour=15, minute="0")
1. By default bot get commits from 00:00 today date if you want change it make changes in function get_query_params from gitlab.py

# Run tests

pip install flake8 pytest pytest-cov
flake8 --count --show-source --statistics review tests
pytest --cov=review --cov-fail-under 80 tests/