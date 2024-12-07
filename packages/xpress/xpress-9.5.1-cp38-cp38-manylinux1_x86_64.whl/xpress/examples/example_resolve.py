# Reads a problem, solves it, then adds a constraint and re-solves it
#
# (C) Fair Isaac Corp., 1983-2024

import xpress

p = xpress.problem()

p.read("example.lp")
p.optimize()
print("solution of the original problem: ", p.getVariable(), "-->",
      p.getSolution())

x = p.getVariable()
p.addConstraint(xpress.Sum(x) <= 1.1)
p.optimize()
print("New solution: ", p.getSolution())
