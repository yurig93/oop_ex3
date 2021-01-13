from math import sqrt
from unittest import TestCase

from location.GeoLocation import GeoLocation


class TestGeoLocation(TestCase):
    def test_distance(self):
        g1 = GeoLocation(1, 1, 1)
        g2 = GeoLocation(2, 2, 2)

        self.assertEqual(g1.distance(g2), sqrt(1 * 1 + 1 * 1 + 1 * 1))
