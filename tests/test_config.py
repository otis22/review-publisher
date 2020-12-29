import unittest
from review.config import parse_projects_channels, parse_stop_words, \
    projects_by_channel


def parse_assert_data():
    return [
       {'project_path': 'repo/path1', 'slack_channel': '#team1'},
       {'project_path': 'repo/path2', 'slack_channel': '#team2'}
    ]


class ConfigCase(unittest.TestCase):

    def test_parse_projects_channels(self):
        self.assertEqual(
            parse_projects_channels("repo/path1#team1,repo/path2#team2"),
            parse_assert_data()
        )

    def test_parse_stop_words_empty(self):
        self.assertEqual(
            parse_stop_words(""),
            []
        )

    def test_parse_stop_words_not_empty(self):
        self.assertEqual(
            parse_stop_words("one,two"),
            ['one', 'two']
        )

    def test_project_by_channel_simple(self):
        test_dict = [
            {'project_path': 'repo/path1', 'slack_channel': '#team1'}
        ]
        self.assertTrue(
            "#team1" in projects_by_channel(test_dict)
        )

    def test_project_by_channel_two_repo_in_one_channel(self):
        test_dict = [
            {'project_path': 'repo/path1', 'slack_channel': '#team1'},
            {'project_path': 'repo/path2', 'slack_channel': '#team1'}
        ]
        self.assertTrue(
            len(
                projects_by_channel(test_dict).get('#team1')
            ) == 2
        )


if __name__ == '__main__':
    unittest.main()
