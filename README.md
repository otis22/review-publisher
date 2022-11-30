# review-publisher

![Build Status](https://github.com/otis22/review-publisher/workflows/CI/badge.svg)


Heroku app for publish commits to slack from gitlab for code review.

In our team all teammate must review all written code, we use slack and gitlab. We've made this stuff. 

## Local start 

```bash
#for quick run
LOCAL=1 GITLAB_URL=u PRIVATE_TOKEN=k PROJECTS_CHANNELS=repo/path1#channel1 BRANCHES=master,develop SLACK_URL=u python main.py
```

```bash
#for test with scheduler
LOCAL=1 GITLAB_URL=u PRIVATE_TOKEN=k PROJECTS_CHANNELS=repo/path1#channel1 BRANCHES=master,develop SLACK_URL=u python cronjob.py
```


## Environments desctription
* LOCAL=1 - Set 1 for local start, it will run job every 30 secs
* GITLAB_URL=u - URL your gitlab 
* PRIVATE_TOKEN=k - Your gitlab private token
* BRANCHES=master,develop - branch for scan commits
* SLACK_URL=u - slack hook url
* COMMIT_TITLE_STOP_WORDS=Merge branch, Merge tag - is not required param for filter commits by title
* SCHEDULE_HOURS - hours for start job, is not required param, 15 by default
* SCHEDULE_DAY_OF_WEEKS - day of week for schedule, is not required param, 'mon-fri' by default, it param for scheduler.add_job(day_of_week=) 
* PROJECTS_CHANNELS=project/path1#slack_channel1,project/path2#slack_channel2 where first part it is project path from gitlab adn second part it is slack channel

## Start on heroku
1. Clone or copy repo
1. In Heroku set envs like screen https://prnt.sc/ubzlks
1. Change schedule in cronjob.py in line scheduler.add_job(send_commits_on_review, 'cron', day_of_week='mon-fri', hour=15, minute="0")
1. By default bot get commits from 00:00 today date if you want change it make changes in function get_query_params from gitlab.py

## For developers 

Install 
```bash
pip install pipenv
pipenv shell
pipenv install --deploy --dev
```

Run tests
```bash
make all
```
