import unittest
from review.slack import get_commits_text, get_commits_payload


class SlackCase(unittest.TestCase):

    def fake_commits(self):
        commits = dict()
        commits['commitid'] = {
            "author_name": 'author_name',
            "title": "title",
            "branch": "master",
            "commit_url": "http://gitlab.com/commitid"
        }
        return commits

    def test_get_commits_text(self):
        self.assertTrue(
            "<http://gitlab.com" in get_commits_text(self.fake_commits())
        )

    def test_get_commits_payload(self):
        self.assertTrue(
            "mychannel" == get_commits_payload("mychannel", self.fake_commits())['channel']
        )


if __name__ == '__main__':
    unittest.main()
