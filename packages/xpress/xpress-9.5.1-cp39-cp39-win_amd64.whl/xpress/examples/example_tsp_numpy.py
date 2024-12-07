# TSP example using numpy functions (for efficiency)
#
# (C) Fair Isaac Corp., 1983-2024

import xpress as xp
import numpy as np

def cb_preintsol(prob, data, soltype, cutoff):
    '''Callback for checking if solution is acceptable
    '''

    n = data
    xsol = prob.getCallbackSolution()
    xsolf = np.array(xsol)      # flattened
    xsol  = xsolf.reshape(n,n)  # matrix-shaped
    nextc = np.argmax(xsol, axis=1)

    i = 0
    ncities = 1

    # Scan cities in order until we get back to 0 or the solution is
    # wrong and we're diverging
    while nextc[i] != 0 and ncities < n:
        ncities += 1
        i = nextc[i]

    reject = False
    if ncities < n:
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
            # Obtain an order by checking the maximum of the variable matrix
            # for each row
            unchecked = np.zeros(n)
            ngroup = 0

            # Initialize the vectors to be passed to addcuts
            cut_mstart = [0]
            cut_ind = []
            cut_coe = []
            cut_rhs = []

            nnz = 0
            ncuts = 0

            while np.min(unchecked) == 0 and ngroup <= n:
                '''Seek a tour
                '''

                ngroup += 1
                firstcity = np.argmin(unchecked)
                assert (unchecked[firstcity] == 0)
                i = firstcity
                ncities = 0
                # Scan cities in order
                while True:
                    unchecked[i] = ngroup  # mark city i with its new group, to be used in addcut
                    ncities += 1
                    i = nextc[i]

                    if i == firstcity or ncities > n + 1:
                        break

                assert ncities < n # we know solutions is infeasible

                # unchecked[unchecked == ngroup] marks nodes to be made part of
                # subtour elimination inequality

                # Find indices of current subtour. S is the set of nodes
                # traversed by the subtour, compS is its complement.
                S     = np.where(unchecked == ngroup)[0].tolist()
                compS = np.where(unchecked != ngroup)[0].tolist()

                indices = [i*n+j for i in S for j in compS]

                # Check if solution violates the cut, and if so add the cut to
                # the list.
                if sum(xsolf[i] for i in indices) < 1 - 1e-3:
                    mcolsp, dvalp = [], []

                    # Presolve cut in order to add it to the presolved problem
                    drhsp, status = prob.presolverow(rowtype='G',
                                                     origcolind=indices,
                                                     origrowcoef=np.ones(len(indices)),
                                                     origrhs=1,
                                                     maxcoefs=prob.attributes.cols,
                                                     colind=mcolsp,
                                                     rowcoef=dvalp)
                    # Since mipdualreductions=0, presolving the cut must succeed, and the cut should
                    # never be relaxed as this would imply that it did not cut off a subtour.
                    assert status == 0

                    nnz += len(mcolsp)
                    ncuts += 1

                    cut_ind.extend(mcolsp)
                    cut_coe.extend(dvalp)
                    cut_rhs.append(drhsp)
                    cut_mstart.append(nnz)

                if ncuts > 0:
                    assert (len(cut_mstart) == ncuts + 1)
                    assert (len(cut_ind) == nnz)

                    prob.addcuts(cuttype=[0] * ncuts,
                                 rowtype=['G'] * ncuts,
                                 rhs=cut_rhs,
                                 start=cut_mstart,
                                 colind=cut_ind,
                                 cutcoef=cut_coe)

    return (reject, None)

def print_sol(p, n):
    '''Print the solution: order of nodes and cost
    '''

    xsol = np.array(p.getSolution()).reshape(n,n)
    nextc = np.argmax(xsol, axis=1)

    i = 0

    # Scan cities in order
    tour = []
    while i != 0 or len(tour) == 0:
        tour.append(str(i))
        i = nextc[i]
    print('->'.join(tour), '->0; cost: ', p.attributes.objval, sep='')


def create_initial_tour(n):
    '''Returns a permuted trivial solution 0->1->2->...->(n-1)->0
    '''
    sol = np.zeros((n, n))
    p = np.random.permutation(n)
    for i in range(n):
        sol[p[i], p[(i + 1) % n]] = 1
    return sol.flatten()


def solve_opttour():
    '''Create a random TSP problem
    '''

    n = 50
    CITIES = range(n)  # set of cities: 0..n-1

    np.random.seed(3)

    X = 100 * np.random.rand(n)
    Y = 100 * np.random.rand(n)

    # Compute distance matrix
    dist = np.ceil(np.sqrt ((X.reshape(n,1) - X.reshape(1,n))**2 +
                            (Y.reshape(n,1) - Y.reshape(1,n))**2))

    p = xp.problem()

    # Create variables as a square matrix of binary variables. Note
    # the use of dtype=xp.npvar (introduced in Xpress 8.9) to ensure
    # NumPy uses the Xpress operations for handling these vectors.
    fly = np.array([p.addVariable(vartype=xp.binary, name='x_{0}_{1}'.format(i,j))
                    for i in CITIES for j in CITIES], dtype=xp.npvar).reshape(n,n)


    # Degree constraints
    p.addConstraint(xp.Sum(fly[i,:]) - fly[i,i] == 1  for i in CITIES)
    p.addConstraint(xp.Sum(fly[:,i]) - fly[i,i] == 1  for i in CITIES)

    # Fix diagonals (i.e. city X -> city X) to zero
    p.addConstraint(fly[i,i] == 0 for i in CITIES)

    # Objective function
    p.setObjective (xp.Sum((dist * fly).flatten()))

    # Add callbacks
    p.addcbpreintsol(cb_preintsol, n)

    # Disable dual reductions (in order not to cut optimal solutions)
    # and nonlinear reductions, in order to be able to presolve the
    # cuts.
    p.controls.mipdualreductions = 0

    # Create 10 trivial solutions: simple tour 0->1->2...->n->0
    # randomly permuted
    for k in range(10):
        InitTour = create_initial_tour(n)
        p.addmipsol(solval=InitTour, name="InitTour_{}".format(k))


    p.optimize()

    if p.attributes.solstatus not in [xp.SolStatus.OPTIMAL, xp.SolStatus.FEASIBLE]:
        print("Solve status:", p.attributes.solvestatus.name)
        print("Solution status:", p.attributes.solstatus.name)
    else:
        print_sol(p,n)  # print solution and cost


if __name__ == '__main__':
    solve_opttour()
