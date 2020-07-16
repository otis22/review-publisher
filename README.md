# review-publisher

![Build Status](https://github.com/otis22/review-publisher/workflows/CI/badge.svg)


Heroku app for publish commit for review

https://saqibameen.com/deploy-python-cron-job-scripts-on-heroku/

# Run tests

pip install flake8 pytest pytest-cov
flake8 --count --show-source --statistics review tests
pytest --cov=review --cov-fail-under 90 tests/