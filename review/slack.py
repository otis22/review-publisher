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


def get_first_payload(channel):
    return get_mrkdwn_payload(channel, "Review time!!!")


def send_commits(commits, hook_url, channel):
    responses = []
    response = requests.post(
        hook_url,
        data=json.dumps(get_first_payload(channel)),
        headers={'Content-Type': "application/json"}
    )
    responses.append(response.text)
    for commit in commits:
        response = requests.post(
            hook_url,
            data=json.dumps(get_commit_payload(channel, commit)),
            headers={'Content-Type': "application/json"}
        )
        responses.append(response.text)

    return "\n".join(responses)
