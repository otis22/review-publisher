import unittest
from review.gitlab import one


class MyTestCase(unittest.TestCase):

    def test_something(self):
        self.assertEqual(True, True)

    def test_gitlab_one(self):
        self.assertEqual(one(2), 4)

    def test_gitlab_one2(self):
        self.assertEqual(one(-2), 0)


if __name__ == '__main__':
    unittest.main()
