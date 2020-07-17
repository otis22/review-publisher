# review-publisher

![Build Status](https://github.com/otis22/review-publisher/workflows/CI/badge.svg)


Heroku app for publish commit for review

## Inspired
https://saqibameen.com/deploy-python-cron-job-scripts-on-heroku/

# Local start 
LOCAL=1 GITLAB_URL=yoururl PRIVATE_TOKEN=token PROJECT_ID=1 BRANCHES=master,develop python cronjob.py


# Run tests

pip install flake8 pytest pytest-cov
flake8 --count --show-source --statistics review tests
pytest --cov=review --cov-fail-under 80 tests/