import unittest
from review.utils import filesize


class UtilsCase(unittest.TestCase):

    def test_sizeof_in_kb(self):
        self.assertEqual(
            filesize(2500),
            '2.4KiB'
        )

    def test_sizeof_in_mb(self):
        self.assertEqual(
            filesize(2500000),
            '2.4MiB'
        )


if __name__ == '__main__':
    unittest.main()
