import os
from review.gitlab import commits_for_branches, get_project_id, \
    commits_for_projects, user_rank_by_total, repo_info
from review.cliq import send_commits, send_user_rank, send_review_time
from review.config import parse_projects_channels, parse_stop_words, \
    projects_by_channel
from review.schedule import Schedule
from datetime import datetime
from backports.zoneinfo import ZoneInfo


def create_schedule_by_settings() -> Schedule:
    hours = os.environ.get('SCHEDULE_HOURS', 15)
    day_of_weeks = os.environ.get('SCHEDULE_DAY_OF_WEEKS', 'mon-fri')
    return Schedule(day_of_weeks, hours)


def now_with_timezone() -> datetime:
    timezone = os.environ.get('TIMEZONE', 'Europe/Kiev')
    return datetime.now(tz=ZoneInfo(timezone))


def get_cliq_url(channel_name: str) -> str:
    company_id = os.environ.get('CLIQ_COMPANY')
    zapikey = os.environ.get('CLIQ_TOKEN')
    return f"https://cliq.zoho.com/company/{company_id}/api/v2/channelsbyname/{channel_name}/message?zapikey={zapikey}"


def send_commits_on_review():
    """
        Job for sending commits from gitlab in Zoho Cliq channel.
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
    private_token = os.environ.get("PRIVATE_TOKEN")
    assert len(private_token) > 0

    for conf in projects_channels:
        project_path = conf['project_path']
        project_id = get_project_id(gitlab_url, private_token, project_path)
        get_commits = commits_for_branches(
            gitlab_url,
            private_token,
            stop_words
        )
        cliq_channel = conf['cliq_channel']
        print(cliq_channel)
        assert len(cliq_channel) > 0

        schedule = create_schedule_by_settings()

        cliq_url = get_cliq_url(cliq_channel)
        print(cliq_url)

        response_review_time = send_review_time(
            repo_info(
                project_id=project_id,
                gitlab_url=gitlab_url,
                private_token=private_token
            ),
            cliq_url,
            cliq_channel
        )

        print(response_review_time)

        response_text = send_commits(
            get_commits(
                project_id=project_id,
                branches=branches,
                project_path=project_path,
                since_date=schedule.since_date(now_with_timezone())
            ),
            cliq_url,
            cliq_channel
        )
        print(response_text)


def send_users_rank_by_gitlab_stats():
    """
        Job for sending users rank by gitlab stats to Zoho Cliq channel.
        Job will find projects for every channel and create rank per channel.
    """
    projects_channels = parse_projects_channels(
        os.environ.get("PROJECTS_CHANNELS")
    )
    assert len(projects_channels) > 0
    stop_words = parse_stop_words(
        os.environ.get("COMMIT_TITLE_STOP_WORDS", "")
    )
    gitlab_url = os.environ.get("GITLAB_URL")
    assert len(gitlab_url) > 0
    private_token = os.environ.get("PRIVATE_TOKEN")
    assert len(private_token) > 0

    channels_with_projects = projects_by_channel(projects_channels)
    get_commits = commits_for_projects(
        gitlab_url,
        private_token,
        stop_words
    )
    for channel_name in channels_with_projects:
        schedule = create_schedule_by_settings()
        rank = user_rank_by_total(
            get_commits(
                channels_with_projects.get(channel_name),
                schedule.since_date(now_with_timezone())
            )
        )
        cliq_url = get_cliq_url(channel_name)
        print(cliq_url)
        print(
            send_user_rank(rank, cliq_url, channel_name)
        )


def main_job():
    send_commits_on_review()
    send_users_rank_by_gitlab_stats()


if __name__ == '__main__':
    main_job()