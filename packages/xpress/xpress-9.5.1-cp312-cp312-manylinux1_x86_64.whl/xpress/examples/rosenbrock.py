# Define the well-known Rosenbrock function and minimize it
#
# (C) Fair Isaac Corp., 1983-2024

import xpress as xp

p = xp.problem()

x = p.addVariable(lb=-xp.infinity)
y = p.addVariable(lb=-xp.infinity)

# parameters of the Rosenbrock function
a = 1
b = 100

p.setObjective((a - x)**2 + b * (y - x**2)**2)

# Solve this problem with a local nonlinear solver.
p.controls.nlpsolver = 1

p.optimize()

print('solution: ', p.getSolution(), '; value: ', p.attributes.objval)
