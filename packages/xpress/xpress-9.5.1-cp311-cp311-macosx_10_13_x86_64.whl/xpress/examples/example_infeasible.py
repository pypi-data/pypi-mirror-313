# Example that shows how to treat an infeasible problem.
#
# (C) Fair Isaac Corp., 1983-2024

import xpress as xp

minf = xp.problem("ex-infeas")

x0 = minf.addVariable()
x1 = minf.addVariable()
x2 = minf.addVariable(vartype=xp.binary)

c1 = x0 + 2 * x1 >= 1
c2 = 2 * x0 + x1 >= 1
c3 = x0 + x1 <= .5

minf.addConstraint(c1, c2, c3)
minf.optimize()
minf.iisall()
print("there are ", minf.attributes.numiis, " iis's")

miisrow = []
miiscol = []
constrainttype = []
colbndtype = []
duals = []
rdcs = []
isolationrows = []
isolationcols = []

# get data for the first IIS

minf.getiisdata(1, miisrow, miiscol, constrainttype, colbndtype,
                duals, rdcs, isolationrows, isolationcols)

print("iis data:", miisrow, miiscol, constrainttype, colbndtype,
      duals, rdcs, isolationrows, isolationcols)

# Another way to check IIS isolations
print("iis isolations:", minf.iisisolations(1))

rowsizes = []
colsizes = []
suminfeas = []
numinfeas = []

print("iisstatus:", minf.iisstatus(rowsizes, colsizes, suminfeas, numinfeas))
print("vectors:", rowsizes, colsizes, suminfeas, numinfeas)
