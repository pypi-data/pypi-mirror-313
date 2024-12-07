# Multi-objective knapsack example
# (c) Fair Isaac Corp., 2024

import xpress as xp
import numpy as np

n = 15            # Number of items
max_weight = 10   # Maximum weight that can be carried

# Random weights and two random value metrics
np.random.seed(123)
weights = np.random.randint(1, 4, n)
values = np.random.randint(1, 6, (2, n))

p = xp.problem()

# Decision variables for each item
take = p.addVariables(n, vartype=xp.binary)

# Total weight cannot exceed maximum weight
ctr = xp.Dot(take, weights) <= max_weight

p.addConstraint(ctr)

# Define the two objectives
p.setObjective(xp.Dot(take, values[0]), objidx=0, priority=2, sense=xp.maximize)
p.setObjective(xp.Dot(take, values[1]), objidx=1, priority=1)

# Solve the problem
p.setOutputEnabled(False)
p.optimize()

if p.attributes.solvestatus == xp.SolveStatus.COMPLETED and p.attributes.solstatus == xp.SolStatus.OPTIMAL:
  print('Problem was solved to optimality')
  sol = p.getSolution(take)
  print('Items selected:', ', '.join(str(i) for i in range(n) if sol[i]))
  print('Total weight:', xp.Dot(sol, weights))
  print('First objective:', p.calcobjn(0))
  print('Second objective:', p.calcobjn(1))
elif p.attributes.solvedobjs == 1:
  print(f'Failed to solve first objective')
else:
  print('Solved first objective but failed to solve second objective')
