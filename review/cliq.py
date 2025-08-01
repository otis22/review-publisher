import requests
import json


def get_commit_text(commit):
    return "{} - [{} / {}]({}) _by {}_".format(
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
        }
    }


def send_review_time(repo_info, cliq_url):
    return requests.post(
        cliq_url,
        data=json.dumps(get_cliq_payload(repo_info)),
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


def send_user_rank(rank, hook_url):
    response = requests.post(
        hook_url,
        data=json.dumps(
            get_user_rank_payload(rank)
        ),
        headers={'Content-Type': "application/json"}
    )
    return response.text