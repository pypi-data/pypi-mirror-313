# Markowitz portfolio optimization
# A multi-objective quadratic programming example

# In Markowitz portfolio optimization there are two objectives: to maximize reward
# while minimizing risk (i.e. variance). This example plots several points on the
# optimal frontier using a blended multi-objective approach, and shows that a point
# computed using a lexicographic approach also lies on this frontier.

# (c) Fair Isaac Corp., 2024

import xpress as xp
import numpy as np
from matplotlib import pyplot as plt

# The historical mean return on investment for five stocks
returns = np.array([0.31, 0.87, 0.31, 0.66, 0.24])

# The historical covariances of the five stocks
covariance = np.array([
  [0.32,  0.70,  0.19,  0.52,  0.16],
  [0.70,  4.35, -0.48, -0.06, -0.03],
  [0.19, -0.48,  0.98,  1.10,  0.10],
  [0.52, -0.6,   1.10,  2.48,  0.37],
  [0.16, -0.3,   0.10,  0.37,  0.31]
])

p = xp.problem()

# Non-negative variables represent percentage of capital to invest in each stock
x = p.addVariables(len(returns))

# All objectives must be linear, so define a free transfer variable for the variance
variance = p.addVariable(lb=-xp.infinity)

ctrs = [
  xp.Sum(x) == 1,                             # Must invest 100% of capital
  xp.Dot(x, covariance, x) - variance <= 0    # Set up transfer variable for variance
]

p.addConstraint(ctrs)

p.addObjective(xp.Dot(x, returns))    # Maximize mean return
p.addObjective(variance)   # Minimize variance

p.setOutputEnabled(False)

# Vary the objective weights to explore the optimal frontier
weights = np.linspace(0.05, 0.95, 20)
means = []
variances = []

for w in weights:
  p.setObjective(objidx=0, weight=w,sense=xp.maximize)  # First objective defines the sense of the problem
  p.setObjective(objidx=1, weight=w-1)  # Reverse the sense by assigning a negative weight because we minimize variance
  p.optimize()
  means.append(xp.Dot(p.getSolution(x), returns).item())
  variances.append(p.getSolution(variance))

# Now we will maximize profit alone, and then minimize variance while not
# sacrificing more than 10% of the maximum profit
p.setObjective(objidx=0, priority=1, weight=1, reltol=0.1,sense=xp.maximize)
p.setObjective(objidx=1, priority=0, weight=-1)
p.optimize()
m0 = xp.Dot(p.getSolution(x), returns).item()
v0 = p.getSolution(variance)

# Plot the optimal frontier and mark the final point that we calculated
plt.plot(means, variances)
plt.plot(m0, v0, c='r', marker='.')
plt.title('Return on investment vs variance')
plt.xlabel('Expected return')
plt.ylabel('Variance')

plt.show()
