from scipy.optimize import minimize
from design_variables import L, B, D, T, Cb
from optimization_function import optimization_function
from constraints import build_bounds, build_constraints


# x0 is the initial guess vector containing ship parameters
x0 = [L, B, D, T, Cb]


# We then apply the optimization by calling the minimize function. See:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
result = minimize(
    x0=x0,  # Passing the initial guess vector
    fun=optimization_function,  # Objective function to be optimized
    method="SLSQP",  # We are using the Sequential Least Squares Programming algorithm
    # Sequence of dictionaries defining the constraints
    constraints=build_constraints(),
    # Sequence of tuples defining lower and upper bounds for each design variable
    bounds=build_bounds(),
)


# Get the Optimized transportation cost and the changed
# ship parameters as result of the optimization
optimized_measure_of_merit = result.fun
L, B, D, T, Cb = result.x


# And finnally print the obtained values
print(
    f"Optimized Measure of merit: {optimized_measure_of_merit} \n")
print(f"Length (L) after optimization: {L} [m]")
print(f"Breadth (B) after optimization: {B} [m]")
print(f"Depth (D) after optimization: {D} [m]")
print(f"Draught (T) after optimization: {T} [m]")
print(f"Block Coefficient (Cb) after optimization: {Cb}")
