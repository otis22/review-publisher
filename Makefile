unit:
	pytest --cov=review --cov-fail-under 80 tests/

style:
	flake8 --count --show-source --statistics review tests main.py cronjob.py

all: unit style

.PHONY: style unit all