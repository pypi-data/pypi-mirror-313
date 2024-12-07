# Construct a problem from scratch with variables of various
# types. Adds indicator constraints and shows how to retrieve
# such data once it has been added to the problem using the
# API functions.
#
# (C) Fair Isaac Corp., 1983-2024

import xpress as xp

m = xp.problem()

m.controls.miprelstop = 0

# All variables used in this example
v1 = m.addVariable(lb=0, ub=10, vartype=xp.continuous)
v2 = m.addVariable(lb=1, ub=7, vartype=xp.continuous)
v3 = m.addVariable(lb=5, ub=10, threshold=7, vartype=xp.semicontinuous)
vb = m.addVariable(vartype=xp.binary)

# Indicator constraints consist of a tuple with a condition on a
# binary variable and a constraint
ind1 = (vb == 0, v1 + v2 >= 6)
ind2 = (vb == 1, v1 + v3 >= 4)

# Adds the first indicator constraint
m.addIndicator(ind1)
# Adds another indicator constraint and the second one defined above
m.addIndicator((vb == 1, v2 + v3 >= 5), ind2)

ind_inds = []
ind_flags = []

# Returns the indicator constraint condition (indicator variable and complement flag) associated to the rows in a given range
m.getindicators(ind_inds, ind_flags, 0, 2)

print("Indicator variables and flags: ", ind_inds, ind_flags)

m.setObjective(xp.Sum(v1,v2,v3))

m.optimize()

print("v1: ", m.getSolution(v1),
      ", v2: ", m.getSolution(v2),
      "; sol vector: ", m.getSolution(),
      "; obj: ", m.attributes.objval,
      sep="")  # default separator between strings is " "