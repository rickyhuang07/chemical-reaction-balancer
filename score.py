from driver import EVERYTHING
from config import MY_FUNCTIONS

import math

from collections import Counter

EV = dict(EVERYTHING)


CATEGORIES = Counter()
for f in EV:
    CATEGORIES[f.split(".")[0]] += 1

possible_points = sum(EV.values()) + 2 * len(CATEGORIES)

print(f"Based on your current configuration, if **all** the tests (not just the ones for your functions) pass, you will earn the following:\n")
points = 0
pre = " "

star = '\u2605'

PER_CATEGORY = Counter()

for func in MY_FUNCTIONS:
    print(f"{pre} {star * EV[func]}{' '*(5 - EV[func])} for {func}")
    pre = "+"
    points += EV[func]
    PER_CATEGORY[func.split(".")[0]] += 1

print("-" * 80)
print(f"= {points}{star} for individual functions")
print("-" * 80)
tackled_points = math.ceil(1.5 * len(PER_CATEGORY))
print(f"+ {tackled_points}{star} for categories tackled")
completed_points = sum(
    [2 if PER_CATEGORY[x] == CATEGORIES[x] else 0 for x in PER_CATEGORY])
print(f"+ {completed_points}{star} for categories completed")
print("-" * 80)

X = round(100 * (points + tackled_points + completed_points) /
          (possible_points - 15), 2)
print(f"= {X}% on the project!")
