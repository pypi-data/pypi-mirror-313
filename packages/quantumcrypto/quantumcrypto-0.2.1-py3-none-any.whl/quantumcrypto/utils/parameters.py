"""
Parameter sets.
"""

from collections import namedtuple


PmSet = namedtuple("pm_set", ["k", "n1", "n2", "du", "dv"])

P512 = PmSet(k=2, n1=3, n2=2, du=10, dv=4)

P768 = PmSet(k=3, n1=2, n2=2, du=10, dv=4)

P1024 = PmSet(k=4, n1=2, n2=2, du=11, dv=5)
