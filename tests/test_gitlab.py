import unittest
from review.gitlab import get_commits_url, get_query_params_by_branch, \
    api_request_creator, commits_for_branches, get_commits_for_branches, \
    commit_url, with_url, valid_commit, get_project_id_by_path, \
    get_projects_url_by_path, get_all_commits, unique_users_from_commit, \
    sum_total_for_user, user_rank_by_total
from datetime import datetime


def fake_request_with_data(fakedata):
    def fakerequest(method, url, params):
        class Response:
            def json(self):
                return fakedata

        return Response()
    return fakerequest


class GitlabCase(unittest.TestCase):

    def test_get_commits_url(self):
        self.assertTrue(
            "http://gitlab.com" in get_commits_url("http://gitlab.com", 1)
        )

    def test_query_string_since(self):
        self.assertTrue(
            datetime.now().strftime('%Y-%m')
            in get_query_params_by_branch("develop", datetime.now())['since']
        )

    def test_query_ref_name(self):
        self.assertTrue(
            "develop" == get_query_params_by_branch(
                "develop",
                datetime.now()
            )['ref_name']
        )

    def test_api_creator(self):
        self.assertTrue(
            "function" in str(type(api_request_creator("secret")))
        )

    def test_commits_by(self):

        self.assertTrue(
            "function" in str(
                type(commits_for_branches("http://gitlab.com", "secret", []))
            )
        )

    def test_get_commits(self):
        fakedata = [
            {
                "id": "id1",
                "short_id": "61f139a1",
                "created_at": "2020-07-16T14:29:25.000Z",
                "parent_ids": [
                    "c027292c4625ec12bade975cfee08bbf476cefc1"
                ],
                "title": "TR-8125 Отображаются не все",
                "message": "TR-8125 Отображаются не все",
                "author_name": "TT",
                "author_email": "gg@gmail.com",
                "authored_date": "2020-07-16T14:29:25.000Z",
                "committer_name": "TT",
                "committer_email": "gg@gmail.com",
                "committed_date": "2020-07-16T14:29:25.000Z"
            },
            {
                "id": "id2",
                "short_id": "c027292c",
                "created_at": "2020-07-16T14:08:26.000Z",
                "parent_ids": [
                    "d5a70bcb6e6d8a8845beb11149f16ad92bec9d68"
                ],
                "title": "review",
                "message": "review\n",
                "author_name": "GT",
                "author_email": "yy@gmail.com",
                "authored_date": "2020-07-16T14:08:26.000Z",
                "committer_name": "FF",
                "committer_email": "gg@gmail.com",
                "committed_date": "2020-07-16T14:08:26.000Z"
            }
        ]

        commits = get_commits_for_branches(
            url="https://fake.url",
            branches=['develop', 'master'],
            request=fake_request_with_data(fakedata),
            since_date=datetime.now()
        )
        self.assertTrue(
            commits[0]['title'] == 'TR-8125 Отображаются не все'
        )

    def test_get_commits_without_doubles(self):
        fakedata = [
            {
                "id": "id1",
                "short_id": "61f139a1",
                "created_at": "2020-07-16T14:29:25.000Z",
                "parent_ids": [
                    "c027292c4625ec12bade975cfee08bbf476cefc1"
                ],
                "title": "TR-8125 Отображаются не все",
                "message": "TR-8125 Отображаются не все",
                "author_name": "TT",
                "author_email": "gg@gmail.com",
                "authored_date": "2020-07-16T14:29:25.000Z",
                "committer_name": "TT",
                "committer_email": "gg@gmail.com",
                "committed_date": "2020-07-16T14:29:25.000Z"
            }
        ]

        commits = get_commits_for_branches(
            url="https://fake.url",
            branches=['develop', 'master'],
            request=fake_request_with_data(fakedata),
            since_date=datetime.now()
        )
        self.assertEqual(len(commits), 1)

    def test_commit_url_has_url(self):
        self.assertTrue(
            "https://fake.url" in commit_url(
                'https://fake.url',
                'path/repo',
                'idcommit'
            )
        )

    def test_commit_url_has_id_commit(self):
        self.assertTrue(
            "idcommit" in commit_url(
                'https://fake.url',
                'path/repo',
                'idcommit'
            )
        )

    def test_commit_with_url(self):
        self.assertTrue(
            "commit_url" in with_url(
                {
                    "title": "some title",
                    "commit_id": "fakeidcommit"
                },
                "https://fake.url",
                "path/repo"
            )
        )

    def test_valid_commit_is_vallid(self):
        self.assertTrue(
            valid_commit(
                {
                    "title": "some"
                },
                ['test']
            )
        )

    def test_valid_commit_is_not_vallid(self):
        self.assertFalse(
            valid_commit(
                {
                    "title": "test"
                },
                ['test']
            )
        )

    def test_valid_commit_with_empty_list_vallid(self):
        self.assertTrue(
            valid_commit(
                {
                    "title": "test"
                },
                []
            )
        )

    def test_get_projects_url_by_path(self):
        test_project_path = "test/mypath"
        self.assertTrue(
            "mypath" in get_projects_url_by_path(
                "http://gitlab.com",
                test_project_path
            )
        )

    def test_get_project_id_by_path_with_valid_path(self):
        right_project_path = "test/rightpath"
        fakedata = [
            {
                "id": 1,
                "path_with_namespace": "test/wrongpath"
            },
            {
                "id": 2,
                "path_with_namespace": right_project_path
            }
        ]

        self.assertEqual(
            2,
            get_project_id_by_path(
                "http://gitlab.com",
                right_project_path,
                fake_request_with_data(fakedata)
            )
        )

    def test_get_project_id_by_path_with_invalid_path(self):
        right_project_path = "test/rightpath"
        fakedata = [
            {
                "id": 1,
                "path_with_namespace": "test/wrongpath"
            },
            {
                "id": 2,
                "path_with_namespace": "test/wrongpath2"
            }
        ]

        with self.assertRaises(Exception):
            get_project_id_by_path(
                "http://gitlab.com",
                right_project_path,
                fake_request_with_data(fakedata)
            )

    def test_get_all_commits_with_stats(self):
        fakedata = [
            {
                "id": "id1",
                "short_id": "61f139a1",
                "created_at": "2020-07-16T14:29:25.000Z",
                "parent_ids": [
                    "c027292c4625ec12bade975cfee08bbf476cefc1"
                ],
                "title": "TR-8125 Отображаются не все",
                "message": "TR-8125 Отображаются не все",
                "author_name": "TT",
                "author_email": "gg@gmail.com",
                "authored_date": "2020-07-16T14:29:25.000Z",
                "committer_name": "TT",
                "committer_email": "gg@gmail.com",
                "committed_date": "2020-07-16T14:29:25.000Z",
                "web_url": "https://some.gg/0f6",
                "stats": {
                    "additions": 6,
                    "deletions": 6,
                    "total": 12
                }
            }
        ]
        commits = get_all_commits(
            url="https://fake.url",
            request=fake_request_with_data(fakedata),
            since_date=datetime.now()
        )
        self.assertTrue(
            commits[0]['total'] == 12
        )

    def test_unique_users_from_commit(self):
        fake_data = [
            {
                "author_name": "TT"
            },
            {
                "author_name": "TT"
            }
        ]
        self.assertEqual(
            len(unique_users_from_commit(fake_data)),
            1
        )

    def test_sum_total_for_user(self):
        fake_data = [
            {
                "author_name": "TT",
                "total": 1
            },
            {
                "author_name": "TT",
                "total": 2
            }
        ]
        self.assertEqual(
            sum_total_for_user(fake_data, "TT"),
            3
        )

    def test_user_rank_by_total(self):
        fake_data = [
            {
                "author_name": "Low rank author",
                "total": 1
            },
            {
                "author_name": "Low rank author",
                "total": 2
            },
            {
                "author_name": "High rank author",
                "total": 4
            },
        ]
        self.assertEqual(
            user_rank_by_total(fake_data)[0].get('author_name'),
            "High rank author"
        )


if __name__ == '__main__':
    unittest.main()
