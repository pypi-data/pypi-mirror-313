# Minimize a polynomial constructed with the Dot product
#
# (C) Fair Isaac Corp., 1983-2024

import xpress as xp
import numpy as np

#
# Generate a random coefficient tensor T of dimension k + 1 and sizes
# n+1 for each dimension except for the first, which is h, then use it
# to create h polynomial constraints. The lhs of each constraint has a
# polynomial of degree k, and not homogeneous as we amend the vector
# of variable with the constant 1. This is accomplished via a single
# dot product.
#

n = 4   # dimension of variable space
h = 3   # number of polynomial constraints
k = 3   # degree of each polynomial

p = xp.problem()

# Vector of n elements: (1, x1, ..., x_{n-1}), declared with NumPy's
# dtype notation for Xpress expressions (to guarantee Xpress
# operations will be used).
x = np.array([1] + [p.addVariable(lb=-10, ub=10) for _ in range(n-1)], dtype=xp.npexpr)

sizes = [n]*k  # creates list [n,n,...,n] of k elements

# Operator * before a list translates the list into its
# (unparenthesized) tuple, i.e., the result is a reshape list of
# argument that looks like (h, n, n, ..., n)

T = np.random.random(h * n ** k).reshape(h, *sizes)

T2list = [x]*k

compact = xp.Dot(T, *T2list) <= 0


p.addConstraint(compact)

# Solve this problem with a local nonlinear solver
p.controls.nlpsolver = 1
p.optimize()
