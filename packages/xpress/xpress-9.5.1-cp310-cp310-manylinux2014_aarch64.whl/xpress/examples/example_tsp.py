# Solve an instance of the TSP with Xpress using callbacks
#
# (C) Fair Isaac Corp., 1983-2024

# Retrieve an example from
#
# http://www.math.uwaterloo.ca/tsp/world/countries.html
#
# and load the TSP instance, then solve it using the Xpress Optimizer
# library with the appropriate callback. Once the optimization is over
# (i.e. the time limit is reached or we find an optimal solution) the
# optimal tour is displayed using matplotlib.

import networkx as nx
import xpress as xp
import re
import math

from matplotlib import pyplot as plt
from urllib.request import urlretrieve

#
# Download instance from TSPLib
#
# Replace with any of the following for a different instance:
#
# ar9152.tsp   (9125 nodes)
# bm33708.tsp (33708 nodes)
# ch71009.tsp (71009 nodes)
# dj38.tsp       (38 nodes)
# eg7146.tsp   (7146 nodes)
# fi10639.tsp (10639 nodes)
# gr9882.tsp   (9882 nodes)
# ho14473.tsp (14473 nodes)
# ei8246.tsp   (8246 nodes)
# ja9847.tsp   (9847 nodes)
# kz9976.tsp   (9976 nodes)
# lu980.tsp     (980 nodes)
# mo14185.tsp (14185 nodes)
# nu3496.tsp   (3496 nodes)
# mu1979.tsp   (1979 nodes)
# pm8079.tsp   (8079 nodes)
# qa194.tsp     (194 nodes)
# rw1621.tsp   (1621 nodes)
# sw24978.tsp (24978 nodes)
# tz6117.tsp   (6117 nodes)
# uy734.tsp     (734 nodes)
# vm22775.tsp (22775 nodes)
# wi29.tsp       (29 nodes)
# ym7663.tsp   (7663 nodes)
# zi929.tsp     (929 nodes)
# ca4663.tsp   (4663 nodes)
# it16862.tsp (16862 nodes)
#

filename = 'wi29.tsp'

urlretrieve('https://www.math.uwaterloo.ca/tsp/world/' + filename, filename)

# Read file consisting of lines of the form "k: x y" where k is the
# point's index while x and y are the coordinates of the point. The
# distances are assumed to be Euclidean.

instance = open(filename, 'r')
coord_section = False
points = {}

G = nx.Graph()

#
# Coordinates of the points in the graph
#

for line in instance.readlines():

    if re.match('NODE_COORD_SECTION.*', line):
        coord_section = True
        continue
    elif re.match('EOF.*', line):
        break

    if coord_section:
        coord = line.split(' ')
        index = int(coord[0])
        cx = float(coord[1])
        cy = float(coord[2])
        points[index] = (cx, cy)
        G.add_node(index, pos=(cx, cy))

instance.close()

print("Downloaded instance, created graph.")

# Callback for checking if the solution forms a tour
#
# Returns a tuple (a,b) with
#
# a: True if the solution is to be rejected, False otherwise
# b: real cutoff value
def cbpreintsol(prob, G, soltype, cutoff):
    """
    Use this function to refuse a solution unless it forms a tour
    """

    # Obtain solution, then start at node 1 to see if the solutions at
    # one form a tour. The vector s is binary as this is a preintsol()
    # callback.

    s = prob.getCallbackSolution()

    reject = False
    nextnode = 1
    tour = []

    while nextnode != 1 or len(tour) == 0:
        # Find the edge leaving nextnode
        edge = None
        for j in V:
            if j != nextnode and s[xind[nextnode, j]] > 0.5:
                edge = x[nextnode, j]
                nextnode = j
                break
        if edge is None:
            break
        tour.append(edge)

    # If there are n arcs in the loop, the solution is feasible
    if len(tour) < n:
        # The tour given by the current solution does not pass through
        # all the nodes and is thus infeasible.
        # If soltype is non-zero then we reject by setting reject=True.
        # If instead soltype is zero then the solution came from an
        # integral node. In this case we can reject by adding a cut
        # that cuts off that solution. Note that we must NOT set
        # reject=True in that case because that would result in just
        # dropping the node, no matter whether we add cuts or not.
        if soltype != 0:
            reject = True
        else:
            # The solution is infeasible and it was obtained from an integral
            # node. In this case we can generate and inject a cut that cuts
            # off this solution so that we don't find it again.

            # Presolve cut in order to add it to the presolved problem
            colind, rowcoef = [], []
            drhsp, status = prob.presolverow(rowtype='L',
                                             origcolind=tour,
                                             origrowcoef=[1] * len(tour),
                                             origrhs=len(tour) - 1,
                                             maxcoefs=prob.attributes.cols,
                                             colind=colind, rowcoef=rowcoef)
            # Since mipdualreductions=0, presolving the cut must succeed, and
            # the cut should never be relaxed as this would imply that it did
            # not cut off a subtour.
            assert status == 0

            prob.addcuts(cuttype=[1],
                         rowtype=['L'],
                         rhs=[drhsp],
                         start=[0, len(colind)],
                         colind=colind,
                         cutcoef=rowcoef)
    # To accept the cutoff, return second element of tuple as None
    return (reject, None)

#
# Formulate problem, set callback function and solve
#

n = len(points)    # number of nodes
V = range(1, n+1)  # set of nodes

# Set of arcs (i.e. all pairs since it is a complete graph)
A = [(i, j) for i in V for j in V if i != j]

p = xp.problem()

x = {(i, j): p.addVariable(name='x_{0}_{1}'.format(i, j),
                           vartype=xp.binary) for (i, j) in A}

conservation_in = [xp.Sum(x[i, j] for j in V if j != i) == 1 for i in V]
conservation_out = [xp.Sum(x[j, i] for j in V if j != i) == 1 for i in V]

p.addConstraint(conservation_in, conservation_out)

xind = {(i, j): p.getIndex(x[i, j]) for (i, j) in x.keys()}

# Objective function: total distance travelled
p.setObjective(xp.Sum(math.sqrt((points[i][0] - points[j][0])**2 +
                                (points[i][1] - points[j][1])**2) * x[i, j]
                      for (i, j) in A))

# Should find a reasonable solution within 20 seconds
p.controls.timelimit = 20

p.addcbpreintsol(cbpreintsol, G, 1)

# Disable dual reductions (in order not to cut optimal solutions)
# and nonlinear reductions, in order to be able to presolve the
# cuts.
p.controls.mipdualreductions = 0

p.optimize()

if p.attributes.solstatus not in [xp.SolStatus.OPTIMAL, xp.SolStatus.FEASIBLE]:
    print("Solve status:", p.attributes.solvestatus.name)
    print("Solution status:", p.attributes.solstatus.name)
else:
    # Read solution and store it in the graph
    sol = p.getSolution()
    try:
        for (i, j) in A:
            if sol[p.getIndex(x[i, j])] > 0.5:
                G.add_edge(i, j)

        # Display best tour found
        pos = nx.get_node_attributes(G, 'pos')

        nx.draw(G, points)  # create a graph with the tour
        plt.show()          # display it interactively
    except:
        print('Could not draw solution')
