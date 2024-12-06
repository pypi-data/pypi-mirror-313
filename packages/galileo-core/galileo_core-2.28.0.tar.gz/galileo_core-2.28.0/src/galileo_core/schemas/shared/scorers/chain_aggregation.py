from enum import Enum


class ChainAggregationStrategy(str, Enum):
    sum = "SUM"
    average = "AVERAGE"
    first = "FIRST"
    last = "LAST"
