# An example of lexicographic goal programming using the Xpress
# multi-objective API.

# A company produces two electrical products, A and B. Both require
# two stages of production: wiring and assembly. The production plan
# must meet several goals:
# 1. A profit of $200
# 2. A contractual requirement of 40 units of product B
# 3. To fully utilize the available wiring department hours
# 4. To avoid overtime in the assembly department

# (c) Fair Isaac Corp., 2024

import xpress as xp

p = xp.problem()

# Decision variables for the number of products to make of each type
produceA = p.addVariable(vartype=xp.integer)
produceB = p.addVariable(vartype=xp.integer)

# Deviational variables
# There is a penalty for both under- and over-utilizing each department
surplus_wiring = p.addVariable()
deficit_wiring = p.addVariable()
surplus_assembly = p.addVariable()
deficit_assembly = p.addVariable()
# There is no penalty for surplus in profit or in production of product B, only for deficits
deficit_profit = p.addVariable()
deficit_productB = p.addVariable()

# Production constraints
constraints = [
  # Meet or exceed profit goal of $200
  # Profit for products A and B are $7 and $6
  7 * produceA + 6 * produceB + deficit_profit >= 200,
  # Meet or exceed production goal for product B
  produceB + deficit_productB >= 40,
  # Utilize wiring department:
  # Products A and B require 2 and 3 hours of wiring
  # 120 hours are available
  2 * produceA + 3 * produceB - surplus_wiring + deficit_wiring == 120,
  # Utilize assembly department:
  # Products A and B require 6 and 5 hours of assembly
  # 300 hours are available
  6 * produceA + 5 * produceB - surplus_assembly + deficit_assembly == 300
]

p.addConstraint(constraints)

# Define objectives to minimize deviations, in priority order
p.setObjective(deficit_profit,                      objidx=0, priority=4, abstol=0, reltol=0)
p.setObjective(deficit_productB,                    objidx=1, priority=3, abstol=0, reltol=0)
p.setObjective(surplus_wiring   + deficit_wiring,   objidx=2, priority=2, abstol=0, reltol=0)
p.setObjective(surplus_assembly + deficit_assembly, objidx=3, priority=1, abstol=0, reltol=0)

p.optimize()

if p.attributes.solvestatus == xp.SolveStatus.COMPLETED and p.attributes.solstatus == xp.SolStatus.OPTIMAL:
  produceA_sol, produceB_sol = p.getSolution(produceA, produceB)
  surplus_wiring_sol, deficit_wiring_sol = p.getSolution(surplus_wiring, deficit_wiring)
  surplus_assembly_sol, deficit_assembly_sol = p.getSolution(surplus_assembly, deficit_assembly)
  deficit_profit_sol, deficit_productB_sol = p.getSolution(deficit_profit, deficit_productB)
  print('Production plan:')
  print(f'Product A: {int(produceA_sol)} units')
  print(f'Product B: {int(produceB_sol)} units')
  print(f'Profit: ${7 * produceA_sol + 6 * produceB_sol}')
  if deficit_profit_sol > 0:
    print(f'Profit goal missed by ${deficit_profit_sol}')
  if deficit_productB_sol > 0:
    print(f'Contractual goal for product B missed by {int(deficit_productB_sol)} units')
  if surplus_wiring_sol > 0:
    print(f'Unused wiring department hours: {surplus_wiring_sol}')
  if deficit_wiring_sol > 0:
    print(f'Wiring department overtime: {deficit_wiring_sol}')
  if surplus_assembly_sol > 0:
    print(f'Unused assembly department hours: {surplus_assembly_sol}')
  if deficit_assembly_sol > 0:
    print(f'Assembly department overtime: {deficit_assembly_sol}')
else:
  print('Problem could not be solved')
