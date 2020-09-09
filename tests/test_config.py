import unittest
from review.config import parse_projects_channels, parse_stop_words


class ConfigCase(unittest.TestCase):

    def parse_assert_data(self):
        return [
               {'project_path': 'repo/path1', 'slack_channel': '#team1'},
               {'project_path': 'repo/path2', 'slack_channel': '#team2'}
               ]

    def test_parse_projects_channels(self):
        self.assertEqual(
            parse_projects_channels("repo/path1#team1,repo/path2#team2"),
            self.parse_assert_data()
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


if __name__ == '__main__':
    unittest.main()
