'''*******************************************************
  * Python Example Problems                             *
  *                                                     *
  * file burglarl.py                                    *
  * Example for the use of the Python language          *
  * (Burglar problem)                                   *
  * -- Formulation of logical constraints --            *
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

# *** Logic constraint:
# *** Either take "vase" and "picture" or "tv" and "video"
#     (but not both pairs).

# * Values within each pair are the same
p.addConstraint(x["vase"] == x["picture"])
p.addConstraint(x["tv"] == x["video"])

# * Choose exactly one pair (uncomment one of the 3 formulations A, B, or C)

# (A) MIP formulation
#  p.addConstraint(x["tv"] == 1 - x["vase"])

# (B) Logic constraint
# Note: Xpress Python interface doesn't use xor.
# Need to introduce extra variable

y = p.addVariable(vartype=xp.binary)

# (C) Alternative logic formulation
p.addIndicator(y == 1, x["tv"] + x["video"] >= 2)
p.addIndicator(y == 0, x["vase"] + x["picture"] >= 2)
p.addConstraint(x["tv"] + x["video"] + x["vase"] + x["picture"] <= 3)

p.optimize()  # Solve the MIP-problem

# Print out the solution
print("Solution:\n Objective: ", p.attributes.objval)
for i in Items:
    print(" x(", i, "): ", p.getSolution(x[i]))
