import os
from review.gitlab import commits_by, get_project_id
from review.slack import send_commits
from review.config import parse_projects_channels, parse_stop_words
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
    projects_channels = parse_projects_channels(
        os.environ.get("PROJECTS_CHANNELS")
    )
    assert len(projects_channels) > 0
    branches = os.environ.get("BRANCHES").split(',')
    assert len(branches) > 0
    stop_words = parse_stop_words(
        os.environ.get("COMMIT_TITLE_STOP_WORDS", "")
    )
    gitlab_url = os.environ.get("GITLAB_URL")
    assert len(gitlab_url) > 0
    slack_url = os.environ.get("SLACK_URL")
    assert len(slack_url) > 0
    private_token = os.environ.get("PRIVATE_TOKEN")
    assert len(private_token) > 0

    for conf in projects_channels:
        project_path = conf['project_path']

        project_id = get_project_id(gitlab_url, private_token, project_path)
        get_commits = commits_by(gitlab_url, private_token, stop_words)

        slack_channel = conf['slack_channel']
        print(slack_channel)
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


if __name__ == '__main__':
    send_commits_on_review()
