import math
from decimal import *


def round_util(n, decimals=Decimal('2')):
    multiplier = Decimal('10') ** decimals
    return math.floor(n * multiplier + Decimal('0.5')) / multiplier
