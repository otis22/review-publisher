import unittest
from review.gitlab import get_commits_url, get_query_params, \
    api_request_creator, commits_by, get_commits, \
    commit_url, with_url, valid_commit


class GitlabCase(unittest.TestCase):

    def test_get_commits_url(self):
        self.assertTrue(
            "http://gitlab.com" in get_commits_url("http://gitlab.com", 1)
        )

    def test_query_string_since(self):
        self.assertTrue(
            "00:00:00" in get_query_params("develop")['since']
        )

    def test_query_ref_name(self):
        self.assertTrue(
            "develop" == get_query_params("develop")['ref_name']
        )

    def test_api_creator(self):
        self.assertTrue(
            "function" in str(type(api_request_creator("secret")))
        )

    def test_commits_by(self):

        self.assertTrue(
            "function" in str(
                type(commits_by("http://gitlab.com", "secret", []))
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

        def fakerequest(method, url, params):
            class Response:
                def json(self):
                    return fakedata
            return Response()

        commits = get_commits(
            url="https://fake.url",
            branches=['develop', 'master'],
            request=fakerequest
        )
        self.assertTrue(
            commits[0]['title'] == 'TR-8125 Отображаются не все'
        )

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


if __name__ == '__main__':
    unittest.main()
