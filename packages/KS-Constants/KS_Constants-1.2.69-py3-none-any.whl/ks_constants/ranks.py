from enum import Enum


class Rank(Enum):
    Bronze = (0, 25)
    Silver = (25, 50)
    Gold = (50, 75)
    Platinum = (75, 95)
    Diamond = (95, 99)
    Master = (99, 100)

    def __init__(self,
                 lower_percentile: int,
                 upper_percentile: int):
        self._lower_percentile = lower_percentile
        self._upper_percentile = upper_percentile

    def lower_percentile(self):
        return self._lower_percentile

    def upper_percentile(self):
        return self._upper_percentile
