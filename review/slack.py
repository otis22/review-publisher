import requests
import json


def get_commit_text(commit):
    return "<{} | *{}* - {}({})>".format(
        commit['commit_url'],
        commit['branch'],
        commit['title'],
        commit['author_name']
    )


def get_mrkdwn_payload(channel, text):
    return {
        "channel": channel,
        "username": "reviewbot",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ],
        "icon_emoji": "ghost"
    }


def get_commit_payload(channel, commit):
    return get_mrkdwn_payload(channel, get_commit_text(commit))


def send_review_time(repo_path, slack_url, slack_chat):
    data = get_mrkdwn_payload(
        slack_chat,
        "Review time for " + repo_path + "!!!"
    )
    return requests.post(
        slack_url,
        data=json.dumps(data),
        headers={'Content-Type': "application/json"}
    )


def send_commits(commits, hook_url, channel):
    responses = []
    for commit in commits:
        response = requests.post(
            hook_url,
            data=json.dumps(get_commit_payload(channel, commit)),
            headers={'Content-Type': "application/json"}
        )
        responses.append(response.text)

    return "\n".join(responses)
