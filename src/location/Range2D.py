from location.GeoLocation import GeoLocation
from location.Range import Range


class Range2D(object):
    def __init__(self, x_range: Range, y_range: Range):
        self.x_range = x_range
        self.y_range = y_range

    def get_ratio(self, geo: GeoLocation):
        x = self.x_range.get_ratio(geo.x)
        y = self.y_range.get_ratio(geo.y)
        return GeoLocation(x, y, 0)

    def from_ratio(self, geo: GeoLocation) -> GeoLocation:
        x = self.x_range.from_ratio(geo.x)
        y = self.y_range.from_ratio(geo.y)
        return GeoLocation(x, y, 0)

    def __repr__(self) -> str:
        return "X: {}, Y: {}".format(self.x_range, self.y_range)
