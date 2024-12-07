'''*******************************************************
  * Python Example Problems                             *
  *                                                     *
  * file burglari.py                                    *
  * Example for the use of the Python language          *
  * (Burglar problem)                                   *
  *                                                     *
  * (c) 2018-2024 Fair Isaac Corporation                *
  *******************************************************'''

import xpress as xp

Items = set(["camera", "necklace", "vase", "picture", "tv", "video",
             "chest", "brick"])  # Index set for items

WTMAX = 102  # Max weight allowed for haul

VALUE = {"camera": 15, "necklace": 100, "vase": 90, "picture": 60,
         "tv": 40, "video": 15, "chest": 10, "brick": 1}

WEIGHT = {"camera": 2, "necklace": 20, "vase": 20, "picture": 30,
          "tv": 40, "video": 30, "chest": 60, "brick": 10}

p = xp.problem()

x = p.addVariables(Items, vartype=xp.binary)  # 1 if we take item i; 0 otherwise

# Objective: maximize total value
p.setObjective(xp.Sum(VALUE[i]*x[i] for i in Items), sense=xp.maximize)

# Weight restriction
p.addConstraint(xp.Sum(WEIGHT[i]*x[i] for i in Items) <= WTMAX)

p.optimize()                   # Solve the MIP-problem

# Print out the solution
print("Solution:\n Objective: ", p.attributes.objval)
for i in Items:
    print(" x(", i, "): ", p.getSolution(x[i]))
