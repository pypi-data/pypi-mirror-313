# Test for the main features of the Xpress Python interface
#
# Adds a vector of N=5 variables and sets constraints and objective. The
# problem is a convex QCQP
#
# (C) Fair Isaac Corp., 1983-2024

import xpress as xp

N = 5
S = range(N)

m = xp.problem("problem 1")

v = [m.addVariable(name="y{0}".format(i)) for i in S]

print("variable:", v)

m.addConstraint(v[i] + v[j] >= 1 for i in range(N - 4) for j in range(i, i+4))
m.addConstraint(xp.Sum([v[i]**2 for i in range(N - 1)]) <= N**2 * v[N - 1]**2)

# Objective overwritten at each setObjective()
m.setObjective(xp.Sum([i*v[i] for i in S]) * (xp.Sum([i*v[i] for i in S])))

m.optimize()

print("solution: ", m.getSolution())
