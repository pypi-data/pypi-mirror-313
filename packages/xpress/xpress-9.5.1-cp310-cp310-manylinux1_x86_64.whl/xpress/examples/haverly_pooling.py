# Pooling example
#
# This example needs commenting before it is suitable for distribution
#
# (C) Fair Isaac Corp., 1983-2024

#----- crudeA ------/--- pool --|
#                  /            |--- finalX
#----- crudeB ----/             |
#                               |--- finalY
#----- crudeC ------------------|

import xpress as xp

p = xp.problem()

crudeA = p.addVariable(name="A", lb=0.0)
crudeB = p.addVariable(name="B", lb=0.0)
crudeC = p.addVariable(name="C", lb=0.0)

crudeC_flowX = p.addVariable(name="CX", lb=0.0)
crudeC_flowY = p.addVariable(name="CY", lb=0.0)

pool_flowX   = p.addVariable(name="PX", lb=0.0)
pool_flowY   = p.addVariable(name="PY", lb=0.0)

finalX = p.addVariable(name="X", lb=0.0, ub=100)
finalY = p.addVariable(name="Y", lb=0.0, ub=200)

poolQ  = p.addVariable(name="poolQ", lb=0.0)

cost    = p.addVariable(name="cost", lb=0.0)
income  = p.addVariable(name="income", lb=0.0)

# cost and income
p.addConstraint(cost   == 6*crudeA + 16*crudeB + 10*crudeC,
                income == 9*finalX + 15*finalY)

# flow balances
p.addConstraint(finalX == pool_flowX + crudeC_flowX,
                finalY == pool_flowY + crudeC_flowY,
                crudeC == crudeC_flowX + crudeC_flowY,
                crudeA + crudeB == pool_flowX + pool_flowY)

# material balances
pool_sulfur = 3*crudeA + crudeB == (pool_flowX + pool_flowY)*poolQ

p.addConstraint(pool_sulfur,
                pool_flowX * poolQ <= 0.5*crudeC_flowX + 2.5*crudeC_flowY,
                pool_flowY * poolQ <= 1.5*pool_flowY - 0.5*crudeC_flowY)

# Solve this problem with a local solver
p.controls.nlpsolver = 1

p.controls.xslp_solver=0

# money
p.setObjective(income - cost,sense=xp.maximize)

p.optimize()

print('solution: income is', p.getSolution(income), 'and cost is', p.getSolution(cost))
