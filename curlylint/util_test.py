import unittest

from .util import flatten


class TestUtil(unittest.TestCase):
    def test_flatten(self):
        self.assertEqual(list(flatten(())), [])
        self.assertEqual(list(flatten([])), [])
        self.assertEqual(list(flatten((1,))), [1])
        self.assertEqual(
            list(flatten([2, [], (), [3, [(4, 5), (6,)]]])), [2, 3, 4, 5, 6]
        )
