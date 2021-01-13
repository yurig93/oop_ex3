from unittest import TestCase

from location.GeoLocation import GeoLocation
from location.Range import Range
from location.Range2D import Range2D


class TestRange2D(TestCase):
    def test_get_ratio(self):
        r2d = Range2D(Range(0,2), Range(0,2))
        point = r2d.get_ratio(GeoLocation(1, 1, 0))
        self.assertEqual(point.x, 0.5)
        self.assertEqual(point.y, 0.5)

    def test_from_ratio(self):
        r2d = Range2D(Range(0,2), Range(0,2))
        point = r2d.from_ratio(GeoLocation(0.5, 0.5, 0))
        self.assertEqual(point.x, 1)
        self.assertEqual(point.y, 1)
