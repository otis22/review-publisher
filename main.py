import os
from review.gitlab import commits_by, get_project_id
from review.slack import send_commits
from review.schedule import Schedule
from datetime import datetime


def create_schedule_by_settings() -> Schedule:
    hours = os.environ.get('SCHEDULE_HOURS', 15)
    day_of_weeks = os.environ.get('SCHEDULE_DAY_OF_WEEKS', 'mon-fri')
    return Schedule(day_of_weeks, hours)


def send_commits_on_review():
    """
    Job for sending commits from gitlab in slack channel
    """
    gitlab_url = os.environ.get("GITLAB_URL")
    project_path = os.environ.get("PROJECT_PATH")
    branches = os.environ.get("BRANCHES").split(',')
    stop_words = os.environ.get("COMMIT_TITLE_STOP_WORDS", "").split(",")
    private_token = os.environ.get("PRIVATE_TOKEN")

    assert len(gitlab_url) > 0
    assert len(branches) > 0

    project_id = get_project_id(gitlab_url, private_token, project_path)
    get_commits = commits_by(gitlab_url, private_token, stop_words)

    slack_url = os.environ.get("SLACK_URL")
    slack_channel = os.environ.get("SLACK_CHANNEL")
    assert len(slack_url) > 0
    assert len(slack_channel) > 0

    schedule = create_schedule_by_settings()

    response_text = send_commits(
        get_commits(
            project_id=project_id,
            branches=branches,
            project_path=project_path,
            since_date=schedule.since_date(datetime.now())
        ),
        slack_url,
        slack_channel
    )
    print(response_text)
