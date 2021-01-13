from unittest import TestCase

from location.Range import Range


class TestRange(TestCase):
    def test_length(self):
        r = Range(2, 4)
        self.assertEqual(2, r.length)

    def test_get_ratio(self):
        r = Range(2, 4)
        self.assertEqual(0.5, r.get_ratio(3))

    def test_from_ratio(self):
        r = Range(2, 4)
        self.assertEqual(3, r.from_ratio(0.5))
