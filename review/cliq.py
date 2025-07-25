import requests
import json


def get_commit_text(commit):
    return "{} - {} / {} ({} by {})".format(
        commit['title'],
        commit['project'],
        commit['branch'],
        commit['commit_url'],
        commit['author_name']
    )


def get_cliq_payload(text):
    return {
        "text": text,
        "bot": {
            "name": "reviewbot",
            "image": "https://www.zoho.com/cliq/help/restapi/images/bot-custom.png"
        },
        "card": {
            "theme": "modern-inline"
        }
    }


def get_commit_payload(commit):
    return get_cliq_payload(get_commit_text(commit))


def send_review_time(repo_info, cliq_url):
    data = get_cliq_payload("Review time for " + repo_info)
    return requests.post(
        cliq_url,
        data=json.dumps(data),
        headers={'Content-Type': "application/json"}
    )


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


def get_user_rank_payload(rank):
    return get_cliq_payload(get_rank_text(rank))


def send_commits(commits, hook_url):
    responses = []
    for commit in commits:
        response = requests.post(
            hook_url,
            data=json.dumps(get_commit_payload(commit)),
            headers={'Content-Type': "application/json"}
        )
        responses.append(response.text)

    return "\n".join(responses)


def send_user_rank(rank, hook_url):
    response = requests.post(
        hook_url,
        data=json.dumps(
            get_user_rank_payload(rank)
        ),
        headers={'Content-Type': "application/json"}
    )
    return response.text