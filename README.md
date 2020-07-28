# review-publisher

![Build Status](https://github.com/otis22/review-publisher/workflows/CI/badge.svg)


Heroku app for publish commit for review

## Inspired
https://saqibameen.com/deploy-python-cron-job-scripts-on-heroku/

## Local start 
LOCAL=1 GITLAB_URL=u PRIVATE_TOKEN=k PROJECT_ID=1 PROJECT_PATH=r/p BRANCHES=master,develop SLACK_URL=u SLACK_CHANNEL=#developers python cronjob.py

## Environments desctription
* LOCAL=1 - Set 1 for local start, it will run job every 30 secs
* GITLAB_URL=u - URL your gitlab 
* PRIVATE_TOKEN=k - Your gitlab private token
* PROJECT_ID=1 - Project id for commit scan, you can see it GET /projects in gitlab api 
* PROJECT_PATH=r/p - Project path like vendor/project, you can see it in project properties
* BRANCHES=master,develop - branch for scan commits
* SLACK_URL=u - slack hook url
* SLACK_CHANNEL=#developers - slack chanel for message
* COMMIT_TITLE_STOP_WORDS=Merge branch, Merge tag - is not required param for filter commits by title
* SCHEDULE_HOURS - hours for start job, is not required param, 15 by default
* SCHEDULE_DAY_OF_WEEKS - day of week for schedule, is not required param, 'mon-fri' by default, it param for scheduler.add_job(day_of_week=) 

## Start on heroku
1. Clone or copy repo
1. In Heroku set envs like screen https://prnt.sc/tjo398
1. Change schedule in cronjob.py in line scheduler.add_job(send_commits_on_review, 'cron', day_of_week='mon-fri', hour=15, minute="0")
1. By default bot get commits from 00:00 today date if you want change it make changes in function get_query_params from gitlab.py

## For developers 

Install 
```bash
pip install pipenv
pip shell
pipenv install --deploy --dev
```

Run tests
```bash
pipenv run check
```
