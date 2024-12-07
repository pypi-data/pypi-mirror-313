'''*******************************************************
  * Python Example Problems                             *
  *                                                     *
  * file burglar.py                                     *
  * Example for the use of the Python language          *
  * (Burglar problem)                                   *
  *                                                     *
  * (c) 2018-2024 Fair Isaac Corporation                *
  *******************************************************'''

import xpress as xp

Items = range(8)

WTMAX = 102  # Max weight allowed for haul

p = xp.problem()

x = [p.addVariable(vartype=xp.binary) for _ in Items]

VALUE = [15, 100, 90, 60, 40, 15, 10, 1]
WEIGHT = [2, 20, 20, 30, 40, 30, 60, 10]

# Objective: maximize total value
p.setObjective(xp.Sum(VALUE[i]*x[i] for i in Items),
               sense=xp.maximize)

# Weight restriction
p.addConstraint(xp.Sum(WEIGHT[i]*x[i] for i in Items) <= WTMAX)

p.optimize()           # Solve the MIP-problem

# Print out the solution
print("Solution:\n Objective: ", p.attributes.objval)
for i in Items:
    print(" x(", i, "): ", p.getSolution(x[i]))
