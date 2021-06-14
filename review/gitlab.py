import requests
from datetime import datetime
from .utils import filesize


def get_commits_url(gitlab_url, project_id):
    return gitlab_url \
           + '/api/v4/projects/' \
           + str(project_id) \
           + '/repository/commits'


def api_request_creator(private_token):
    headers = {
        'private-token': private_token
    }

    def gitlab_api_request(method, url, params):
        return requests.request(
            method=method,
            headers=headers,
            url=url,
            params=params
        )

    return gitlab_api_request


def get_query_params_by_branch(ref_name: str, since_date: datetime):
    return {
        "ref_name": ref_name,
        "since": since_date.isoformat()
    }


def commits_from_all_pages(url, params, request):
    def all_commits(prev_commits, page):
        print('page', page)
        params['page'] = page
        response = request(
            method="GET",
            url=url,
            params=params
        )
        commits_list = prev_commits + response.json()
        if response.headers.get('X-Next-Page', False):
            return all_commits(
                commits_list,
                response.headers.get('X-Next-Page')
            )
        return commits_list

    return all_commits([], 1)


def get_commits_for_branches(url, branches, request, since_date: datetime):
    commits = []
    id_cache = []
    for branch in branches:
        commits_from_api = commits_from_all_pages(
            request=request,
            url=url,
            params=get_query_params_by_branch(branch, since_date)
        )
        for commit in commits_from_api:
            if commit['id'] in id_cache:
                continue
            id_cache.append(commit['id'])
            commits.append({
                "author_name": commit['author_name'],
                "title": commit["title"],
                "branch": branch,
                "commit_id": commit['id']
            })
    return commits


def get_query_params_all_with_stats(since_date: datetime):
    return {
        "since": since_date.isoformat(),
        "all": True,
        "with_stats": True,
        "first_parent": True
    }


def get_all_commits(url, request, since_date: datetime):
    commits = []
    commits_from_api = commits_from_all_pages(
        request=request,
        url=url,
        params=get_query_params_all_with_stats(since_date)
    )
    for commit in commits_from_api:
        commits.append({
            "author_name": commit['author_name'],
            "title": commit["title"],
            "commit_id": commit['id'],
            "total": commit.get('stats').get('total')
        })
    return commits


def commit_url(gitlab_url, project_path, commit_id):
    return gitlab_url + '/' + project_path + '/commit/' + commit_id


def extra_info(commit, gitlab_url, project_path):
    commit['commit_url'] = commit_url(
        gitlab_url,
        project_path,
        commit['commit_id']
    )
    commit['project'] = project_path
    return commit


def valid_commit(commit, stop_words):
    return all(map(lambda x: x not in commit['title'], stop_words))


def commits_for_branches(
        gitlab_url: str,
        private_token: str,
        stop_words: list
):
    request = api_request_creator(private_token)

    def func_get_commits_by(project_id, project_path, branches, since_date):
        return filter(
            lambda commit: valid_commit(commit, stop_words),
            map(
                lambda commit: extra_info(commit, gitlab_url, project_path),
                get_commits_for_branches(
                    get_commits_url(
                        gitlab_url,
                        project_id
                    ),
                    branches,
                    request,
                    since_date
                )
            )
        )

    return func_get_commits_by


def commits_for_projects(
        gitlab_url: str,
        private_token: str,
        stop_words: list
):
    request = api_request_creator(private_token)

    def func_get_commits_by_projects(projects, since_date):
        commits = []
        for project_path in projects:
            project_id = get_project_id(
                gitlab_url,
                private_token,
                project_path
            )
            commits.extend(
                get_all_commits(
                    get_commits_url(
                        gitlab_url,
                        project_id
                    ),
                    request,
                    since_date
                )
            )
        return filter(
            lambda commit: valid_commit(commit, stop_words),
            commits
        )

    return func_get_commits_by_projects


def get_projects_url_by_path(gitlab_url, project_path):
    assert "/" in project_path
    project_name = project_path.split("/")[1]
    return gitlab_url \
        + 'api/v4/projects?search=' \
        + project_name


def get_project_id_by_path(gitlab_url, project_path, request):
    response = request(
        "GET",
        get_projects_url_by_path(gitlab_url, project_path),
        None
    )
    for project in response.json():
        if project['path_with_namespace'] == project_path:
            return project['id']
    raise Exception("Can`t find project by path")


def get_project_id(gitlab_url, private_token, project_path):
    request = api_request_creator(private_token)
    return get_project_id_by_path(
        gitlab_url,
        project_path,
        request
    )


def unique_users_from_commit(commits):
    return set(el['author_name'] for el in commits)


def sum_total_for_user(commits, user_name):
    return sum(
        map(
            lambda commit: commit['total'],
            filter(
                lambda x: x['author_name'] == user_name,
                commits
            )
        )
    )


def get_repo_data(request, gitlab_url, project_id):
    return request(
        method='GET',
        url=gitlab_url + '/api/v4/projects/' + str(project_id),
        params={'statistics': True}
    ).json()


def formated_repo_info(repo_data):
    return "{}(Size: {}, Wiki Size: {})!".format(
        repo_data['path_with_namespace'],
        filesize(repo_data['statistics']['repository_size']),
        filesize(repo_data['statistics']['wiki_size'])
    )


def repo_info(project_id, gitlab_url, private_token):
    request = api_request_creator(private_token)
    return formated_repo_info(
        get_repo_data(request, gitlab_url, project_id)
    )


def total_per_users(commits):
    commits_list = list(commits)

    def user_row(user_name):
        return {
            "author_name": user_name,
            "total": sum_total_for_user(commits_list, user_name)
        }

    return map(
        lambda user_name: user_row(user_name),
        unique_users_from_commit(commits_list)
    )


def user_rank_by_total(commits):
    not_ranked = list(total_per_users(commits))
    not_ranked.sort(key=lambda x: x['total'], reverse=True)
    return not_ranked
