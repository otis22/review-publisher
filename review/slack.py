import requests
import json


def get_commit_text(commit):
    return "<{} | *{}/{}* - {}({})>".format(
        commit['commit_url'],
        commit['project'],
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


def add_rank_number(rank):
    def add_rank(row, rank_number):
        row['rank'] = rank_number
        return row
    return map(lambda x: add_rank(x[1], x[0]), enumerate(rank))


def get_user_rank_text(row):
    return "{}. {} {}".format(
        row['rank'] + 1,
        row['author_name'],
        row['total']
    )


def get_rank_text(rank):
    return "Users Rating: \n" + "\n".join(
        map(
            lambda x: get_user_rank_text(x),
            add_rank_number(rank)
        )
    )


def get_user_rank_payload(channel, rank):
    return get_mrkdwn_payload(
        channel,
        get_rank_text(rank)
    )


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


def send_user_rank(rank, hook_url, channel):
    response = requests.post(
        hook_url,
        data=json.dumps(
            get_user_rank_payload(channel, rank)
        ),
        headers={'Content-Type': "application/json"}
    )
    return response.text
