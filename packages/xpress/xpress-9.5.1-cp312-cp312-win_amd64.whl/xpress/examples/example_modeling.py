# Demonstrate how variables, or arrays thereof, and constraints, or
# arrays of constraints, can be added into a problem. Prints the
# solution and attributes of the problem.
#
# (C) Fair Isaac Corp., 1983-2024

import xpress as xp

N = 4
S = range(N)

m = xp.problem()

# adds both v, a vector (list) of variables, and v1 and v2, two scalar
# variables.
v = [m.addVariable(name="y{0}".format(i), lb=0, ub=2*N) for i in S]

v1 = m.addVariable(name="v1", lb=0, ub=10, vartype=xp.continuous)
v2 = m.addVariable(name="v2", lb=1, ub=7, threshold=3, vartype=xp.semicontinuous)
vb = m.addVariable(name="vb", vartype=xp.binary)

c1 = v1 + v2 >= 5

m.addConstraint(c1,  # Adds a list of constraints: three single constraints...
                2*v1 + 3*v2 >= 5,
                v[0] + v[2] >= 1,
                # ... and a set of constraints indexed by all {i in
                # S: i<N-1} (recall that ranges in Python are from 0
                # to n-1)
                (v[i+1] >= v[i] + 1 for i in S if i < N-1))

# objective overwritten at each setObjective()
m.setObjective(xp.Sum([i*v[i] for i in S]), sense=xp.minimize)

solvestatus, solstatus = m.optimize()

print("solve status: ", m.attributes.solvestatus.name)
print("solution status: ", m.attributes.solstatus.name)

print("solution:", m.getSolution())
