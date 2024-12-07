# Python equivalent of the ComplexUserFunction.c example in
# examples/nonlinear/c directory
#
# (C) Fair Isaac Corp., 1983-2024

# Define objective and constraint as user functions that return
# derivatives
#
# Minimize myobj (y,z,v,w)
#   s.t.
#   ball (x,t) <= 730
#   1 <= x <= 2
#   2 <= y <= 3
#   3 <= z <= 4
#   4 <= v <= 5
#   5 <= w <= 6
#
# where
#
# myobj (y,z,v,w) = y**2 + z - v + w**2
# ball  (x,t) = x**2 + t**2

import xpress


def myobj(y, z, v, w):
    '''Return value of the objective function with the derivative w.r.t. all variables passed
    '''
    return (y**2 + z - v + w**2,  # value of the function
            2*y,  # derivative w.r.t. y
            1,    # derivative w.r.t. z
            -1,   # derivative w.r.t. v
            2*w)  # derivative w.r.t. w


def ball(x, t):
    '''Return value of the left-hand side of the constraint with its derivatives
    '''
    return (x**2 + t**2,
            2*x,
            2*t)


def myobj_noderiv(y, z, v, w):
    '''Return objective without derivatives
    '''
    return (y**2 + z - v + w**2)  # value of the function


def ball_noderiv(x, t):
    '''Return left-hand side of constraint without derivatives
    '''
    return (x**2 + t**2)


def solve_problem(incder):
    """Construct and solve the problem with or without derivatives

    :param incder: True for including derivatives, False otherwise
    :return:
    """
    p = xpress.problem()

    x = p.addVariable(lb=1, ub=2)
    y = p.addVariable(lb=2, ub=3)
    z = p.addVariable(lb=3, ub=4)
    v = p.addVariable(lb=4, ub=5)
    w = p.addVariable(lb=5, ub=6)

    t = p.addVariable(lb=-xpress.infinity)  # free variable

    p.setObjective(t)

    if incder:
        p.addConstraint(t == xpress.user(myobj, y, z, v, w, derivatives=True))
        p.addConstraint(xpress.user(ball, x, t, derivatives=True) <= 730)
        print('Solving problem using derivatives:')
    else:
        p.addConstraint(t == xpress.user(myobj_noderiv, y, z, v, w))
        p.addConstraint(xpress.user(ball_noderiv, x, t) <= 730)
        print('Solving problem without using derivatives:')

    # With user functions the problem cannot be solved to
    # global optimality, so the control below is not necessary
    # but shown here for completeness. Setting nlpsolver to one
    # ensures the problem is solved by a local solver rather than the
    # global solver.
    p.controls.nlpsolver = 1
    p.optimize()

    print('Problem solved. Objective:', p.attributes.objval, '; solution:', p.getSolution())


if __name__ == '__main__':
    solve_problem(True)
    solve_problem(False)
