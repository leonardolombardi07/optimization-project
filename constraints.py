from numerical_model.volumes import get_height_of_superstructure
from numerical_model.stability import get_GMt


def build_constraints():
    '''A function that builds constraints relating two or more parameters
    or bounds that need to be calculated from the set of parameters (x0 or x)


    Returns
    -------
    out : sequence, dict
        Sequence of dictionaries, each representing a specif constraint
        and containing the keys "type" and "fun".

        "type" : {"eq", "ineq"}
            Determines if it is an equality or inequality constraint

        "fun" : callable
            The function defining the constraint. It receives a vector x with
            all parameters (in the order as defined by the initial guess, x0).
            Equality constraint means that the constraint function result is to
            be zero (fun(x) == 0) whereas inequality means that it is to be
            non-negative (f(x) >= 0).

    See Also
    --------
    https://stackoverflow.com/questions/42303470/scipy-optimize-inequality-constraint-which-side-of-the-inequality-is-considere/42304099

    Notes
    -----
    Constraints typically don't need a builder function like this and are
    more succinctly defined with "func" being a lambda function. The decision to
    create the build_constraints function was to try to make it easier to understand
    how constraints are defined in Scipy and to clarify where each constraint of the
    problem was defined.
    '''

    # ---- TECHNICAL ---- #

    def stability_constraint(x):
        '''GMt >= 0.15'''
        B, D, T, Cb = x[1], x[2], x[3], x[4]
        GMt = get_GMt(T, Cb, B, D)
        return GMt - 0.15  # >= 0

    def superstructure_height_constraint(x):
        '''Total height <= 70'''
        L, B, D, T = x[0], x[1], x[2], x[3]
        Hs = get_height_of_superstructure(L, B)
        total_height = (D + Hs + T)
        return 70 - total_height  # >= 0

    # ---- RATIOS ---- #

    def L_over_D_min(x):
        '''L/D >= 20'''
        L, D = x[0], x[2]
        return L/D - 20  # >= 0

    def L_over_D_max(x):
        '''L/D <= 40'''
        L, D = x[0], x[2]
        return 40 - L/D  # >= 0

    def L_over_B_min(x):
        '''L/B >= 5'''
        L, B = x[0], x[1]
        return L/B - 5  # >= 0

    def L_over_B_max(x):
        '''L/V <= 9'''
        L, B = x[0], x[1]
        return 9 - L/B  # >= 0

    def T_over_D_max(x):
        '''T/D <= 0.75'''
        D, T = x[2], x[3]
        return 0.75 - T/D  # >= 0

    return (
        # Technical
        {'type': 'ineq', 'fun': stability_constraint},
        {'type': 'ineq', 'fun': superstructure_height_constraint},

        # Ratios
        {'type': 'ineq', 'fun': L_over_D_min},
        {'type': 'ineq', 'fun': L_over_D_max},
        {'type': 'ineq', 'fun': L_over_B_min},
        {'type': 'ineq', 'fun': L_over_B_max},
        {'type': 'ineq', 'fun': T_over_D_max},
    )


def build_bounds():
    '''A function that defines bounds for each parameter of the optimization
   problem.


    Returns
    -------
    out : sequence, tup
        Sequence of tuples, each representing the minimum and maximum bounds
        for a specific parameter.

    Notes
    -----
    The order of the bounds of the returned sequence must match the order of
    the initial guess vector (x0) defined. The value "None" represents the
    absence of a minimum or maximum bound.
    '''

    L_bound = (150, 315)  # Min From Database, Max From Ponta Delgada Port
    B_bound = (20, 60)  # From Database
    D_bound = (8, 18)  # From Database
    T_bound = (5, 15)  # From Database
    Cb_bound = (0.55, 0.9)  # From Molland reference & Database

    return (
        L_bound,
        B_bound,
        D_bound,
        T_bound,
        Cb_bound,
    )
