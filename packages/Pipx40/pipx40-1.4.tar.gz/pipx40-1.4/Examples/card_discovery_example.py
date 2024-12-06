from __future__ import print_function
from Pipx40 import *

#Initialising Base Class
base = pipx40_base()

# Return the number of available cards
count = base.CountFreeCards()

print("Found", count, "free cards.")

# Return a list of free cards
list = base.FindFreeCards()

for index, card in enumerate(list):
    print("Card", index + 1, ":", card)
