# Construct a problem from scratch with variables of various
# types. Adds Special Ordered Sets (SOSs) and shows how to
# retrieve such data once it has been added to the problem
# using the API functions.
#
# (C) Fair Isaac Corp., 1983-2024

import xpress as xp

m = xp.problem()

m.controls.miprelstop = 0

# All variables used in this example
v1 = m.addVariable(lb=0, ub=7, vartype=xp.continuous)
v2 = m.addVariable(lb=1, ub=10, threshold=7, vartype=xp.semicontinuous)
y = [m.addVariable(name="y{0}".format(i)) for i in range(2)]

m.addConstraint(v1 + v2 >= xp.Sum(y[i] for i in range(2)))

# Adds an SOS type 1 constraint
s = m.addSOS([v1, v2], [1, 0], name="mynewsos", type=1)

print("SOS:", s.name, s)

m.setObjective(xp.Sum([y[i] for i in range(2)]), sense=xp.maximize)

m.optimize()

print("v1: ", m.getSolution(v1),
      ", v2: ", m.getSolution(v2),
      "; sol vector: ", m.getSolution(),
      "; obj: ", m.attributes.objval,
      sep="")  # default separator between strings is " "

# Adds yet another constraint to the problem and saves it, then
# removes an SOS and saves another version

m.addConstraint((1.25 * v1 - 2.5*v2 + 4.3) * (3.1 * v2 - 2 * v1 - 5.2)
                + 72.5 * v1**2 + 73 * v2**2 <= 1950)

m.write("restriction", "lp")

m.delSOS(s)
m.write("restriction-noSOS", "lp")

m.optimize()
