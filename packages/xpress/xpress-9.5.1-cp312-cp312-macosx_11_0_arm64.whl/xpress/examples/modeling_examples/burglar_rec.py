'''******************************************************
   Python Example Problems

   file burglar_rec.py

   (c) 2018-2024 Fair Isaac Corporation
*******************************************************'''

import xpress as xp
from Data.burglar_rec_dat import I

WTMAX = 102  # Maximum weight allowed
ITEMS = set(["camera", "necklace", "vase", "picture", "tv", "video",
             "chest", "brick"])  # Index set for items

p = xp.problem()

take = {i: p.addVariable(vartype=xp.binary) for i in I.keys()}

# Objective: maximize total value
p.setObjective(xp.Sum(I[i][0] * take[i] for i in ITEMS),
               sense=xp.maximize)

# Weight restriction
p.addConstraint(xp.Sum(I[i][0] * take[i] for i in ITEMS) <= WTMAX)

p.optimize()  # Solve the MIP-problem

# Print out the solution
print("Solution:\n Objective: ", p.attributes.objval)
for i in ITEMS:
    print(" take(", i, "): ", p.getSolution(take[i]))
