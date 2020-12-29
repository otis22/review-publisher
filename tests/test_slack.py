import unittest
from review.slack import get_commit_text, get_commit_payload, \
    get_mrkdwn_payload, get_rank_text


class SlackCase(unittest.TestCase):

    def fake_commit(self):
        return {
            "author_name": 'author_name',
            "project": "project/name",
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

    def test_get_rank_text(self):
        fake_data = [
            {"author_name": "user1", "total": 5},
            {"author_name": "user2", "total": 1}
        ]
        print(get_rank_text(fake_data))
        self.assertTrue(
            "1. user1 5" in get_rank_text(fake_data)
        )

if __name__ == '__main__':
    unittest.main()
