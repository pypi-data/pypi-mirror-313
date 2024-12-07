'''*******************************************************
  * Python Example Problems                             *
  *                                                     *
  * file chess2.py                                      *
  * Example for the use of the Python language          *
  * (Small LP-problem)                                  *
  *                                                     *
  * (c) 2018-2024 Fair Isaac Corporation                *
  *******************************************************'''

import xpress as xp

DescrV = {}
DescrC = {}

p = xp.problem()

xs = p.addVariable()
xl = p.addVariable()

mc_time = 3*xs + 2*xl <= 400  # Limit on available machine time
wood = xs + 3*xl <= 200  # Limit on available wood

# Define the variable and constraint descriptions. Since the arrays
# and the indexing sets are dynamic they grow with each new variable
# description added:
DescrV = {xs: " Number of small chess sets",
          xl: " Number of large chess sets"}

DescrC = {mc_time: " Limit on available machine time",
          wood: " Limit on available wood"}

p.addConstraint(mc_time, wood)

# Define the objective function
p.setObjective(5*xs + 20*xl, sense=xp.maximize)

p.optimize()

rhs = []
p.getrhs(rhs, 0, p.attributes.rows - 1)

# Print out the solution
print("Solution:\n Objective: ", p.attributes.objval)
print(DescrV[xs], ":", p.getSolution(xs), ",",
      DescrV[xl], ":", p.getSolution(xl))

print(" Constraint activity:")
print(DescrC[mc_time], ": ", rhs[p.getIndex(mc_time)] - p.getSlacks(mc_time), "\n",
      DescrC[wood],    ": ", rhs[p.getIndex(wood)]    - p.getSlacks(wood), sep='')
