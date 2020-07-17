import requests
import json


def get_commits_text(commits):
    return "\n".join(
        [
            "<{} | *{}* - {}({})>".format(
                commits[k]['commit_url'],
                commits[k]['branch'],
                commits[k]['title'],
                commits[k]['author_name']
            ) for k in commits
        ]
    )


def get_commits_payload(channel, commits):
    return {
        "channel": channel,
        "username": "reviewbot",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Review Time!!! \n " + get_commits_text(commits)
                }
            }
        ],
        "icon_emoji": "ghost"
    }


def send_commits(commits, hook_url, channel):
    print(json.dumps(get_commits_payload(channel, commits)))
    response = requests.post(
        hook_url,
        data=json.dumps(get_commits_payload(channel, commits)),
        headers={'Content-Type': "application/json"}
    )
    return response.text
