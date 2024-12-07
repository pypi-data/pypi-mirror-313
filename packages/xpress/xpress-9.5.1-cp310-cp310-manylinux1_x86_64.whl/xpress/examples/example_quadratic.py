# Solve a simple quadratic optimization problem. Given a matrix
# Q and a point x0, minimize the quadratic function
#
# x' (Q + alpha I) x
#
# subject to the linear system Q (x - x0) = 1 and nonnegativity on all
# variables. Report solution if available
#
# (C) Fair Isaac Corp., 1983-2024

import xpress as xp
import numpy as np

N = 10

p = xp.problem()

Q = np.arange(1, N**2 + 1).reshape(N, N)
x = p.addVariables(N)
x0 = np.random.random(N)

# c1 and c2 are two systems of constraints of size N each written as
#
# (x-x0)' Q = 1
#
# Qx >= 0

c1 = - xp.Dot((x - x0), Q) == 1
c2 = xp.Dot(Q, x) >= 0

# The objective function is quadratic

p.addConstraint(c1, c2)
p.setObjective(xp.Dot(x, Q + N**3 * np.eye(N), x))

# Compact (equivalent) construction of the problem
#
# p = xp.problem(x, c1, c2, xp.Dot(x, Q + N**3 * np.eye(N), x))

p.optimize("")

print("nrows, ncols:", p.attributes.rows, p.attributes.cols)
print("solution:", p.getSolution())

p.write("test5-qp", "lp")
