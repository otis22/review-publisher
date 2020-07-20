import unittest
from review.slack import get_commit_text, get_commit_payload, \
    get_mrkdwn_payload, get_first_payload


class SlackCase(unittest.TestCase):

    def fake_commit(self):
        return {
            "author_name": 'author_name',
            "title": "title",
            "branch": "master",
            "commit_url": "http://gitlab.com/commitid"
        }

    def test_get_commit_text(self):
        self.assertTrue(
            "<http://gitlab.com" in get_commit_text(self.fake_commit())
        )

    def test_get_mrkdwn_payload(self):
        self.assertTrue(
            'testtext' in str(get_mrkdwn_payload('channel', 'testtext'))
        )

    def test_get_commits_payload(self):
        self.assertTrue(
            "http://gitlab.com/commitid" in str(
                get_commit_payload(
                    "mychannel",
                    self.fake_commit()
                )
            )
        )

    def test_get_first_payload(self):
        self.assertTrue(
            "mychannel" in str(
                get_first_payload("mychannel")
            )
        )


if __name__ == '__main__':
    unittest.main()
