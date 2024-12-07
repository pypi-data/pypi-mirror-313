'''*******************************************************
  * Python Example Problems                             *
  *                                                     *
  * file fstns.py                                       *
  * Example for the use of the Python language          *
  * (Firestation siting problem)                        *
  *                                                     *
  * (c) 2018-2024 Fair Isaac Corporation                *
  *******************************************************'''

import xpress as xp

RTown = range(6)  # Range of towns
TIMELIMIT = 20    # Max. time allowed to reach any town

TIME = [[0, 15, 25, 35, 35, 25], [15, 0, 30, 40, 25, 15],
        [25, 30, 0, 20, 30, 25], [35, 40, 20, 0, 20, 30],
        [35, 25, 35, 20, 0, 19], [25, 15, 25, 30, 19, 0]]

'''This sets SERVE(t,s) to true if the time between the two towns is
   within the time limit. We can then use SERVE to define a set of
   constraints (see below). It is as well possible not to use the
   array SERVE and move the test directly into the definition of the
   constraints.
'''

SERVE = [[TIME[t][s] <= TIMELIMIT for t in RTown] for s in RTown]

p = xp.problem()

# 1 if ambulance at town; 0 if not
openst = [p.addVariable(vartype=xp.binary) for _ in RTown]

# Objective: minimize number fire stations
p.setObjective(xp.Sum(openst[s] for s in RTown))

# Serve each town t by an open station s
p.addConstraint(xp.Sum(openst[s] for s in RTown if SERVE[t][s]) >= 1
                for t in RTown)

p.optimize()  # Solve the MIP-problem

# Print out the solution
print("Solution:\n Minimum number of firestations: ", p.attributes.objval)
for s in RTown:
    print(" open(", s, "): ", p.getSolution(openst[s]), sep='')
print("\n      ", end='')
for s in RTown:
    print(s, " ", end='', sep='')
print('')
for t in RTown:
    if p.getSolution(openst[t]) == 1:
        print(" ", t, ": ", end='')
        for s in RTown:
            if SERVE[t][s]:
                print("Y ", end='')
            else:
                print(". ", end='')
        print('')
