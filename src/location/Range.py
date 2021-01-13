class Range(object):
    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max

    @property
    def length(self):
        return self.max - self.min

    def get_ratio(self, val: float) -> float:
        '''
        Get ration by value.
        :param val:
        :return: A value between 0-1 (if in bounds).
        '''
        return (val - self.min) / self.length

    def from_ratio(self, ratio: float):
        '''
        Gets a value by ratio
        :param ratio: Value between 0-1.
        :return: Value by ratio.
        '''
        return self.min + ratio * self.length

    def __repr__(self) -> str:
        return "{},{}".format(self.min, self.max)
