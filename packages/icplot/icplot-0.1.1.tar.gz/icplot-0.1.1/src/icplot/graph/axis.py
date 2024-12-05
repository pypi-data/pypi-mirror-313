"""
This module has a plot's axis
"""

from pydantic import BaseModel


class Range(BaseModel):
    """
    This is a sequence of numbers specified by lower and upper
    bounds and a step size. Eg (1, 5, 1) gives: [1, 2, 3, 4]
    """

    lower: int
    upper: int
    step: int

    def eval(self) -> list:
        return list(range(self.lower, self.upper, self.step))


class PlotAxis(BaseModel):
    """
    This is a plot's axis
    """

    label: str = ""
    ticks: Range | None = None

    @property
    def resolved_ticks(self) -> list:
        if self.ticks:
            return self.ticks.eval()
        return []
