'''*******************************************************
  * Python Example Problems                             *
  *                                                     *
  * file chess.py                                       *
  * Example for the use of the Python language          *
  * (Small LP-problem)                                  *
  *                                                     *
  * (c) 2018-2024 Fair Isaac Corporation                *
  *******************************************************'''

import xpress as xp

p = xp.problem()

small = p.addVariable()
large = p.addVariable()

# Now we have the constraints

p.addConstraint(3*small + 2*large <= 400)  # limit on available machine time
p.addConstraint(small + 3*large <= 200)  # limit on available wood

# Define the objective function
p.setObjective(5*small + 20*large, sense=xp.maximize)

p.optimize()

print('')
print("Here are the LP results")
print("Objective value is ", p.attributes.objval)
print("Make ", p.getSolution(small), " small sets, and ",
      p.getSolution(large), " large sets")

p.chgcoltype([small, large], ['I', 'I'])

p.optimize()

print('')
print("Here are the IP results")
print("Objective value is ", p.attributes.objval)
print("Make ", p.getSolution(small), " small sets, and ",
      p.getSolution(large), " large sets")
