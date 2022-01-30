from voyage_model.constants import round_trips_per_year
from voyage_model.costs import get_fuel_cost_per_roundtrip, get_port_cost_per_roundtrip
from numerical_model.propulsion import get_power
from numerical_model.volumes import get_gross_tonnage
from numerical_model.weights import get_lightship_weight, get_machinery_weight, get_outfit_weight, get_steel_weight
from numerical_model.costs import get_ship_cost


def optimization_function(x):
    '''A function that calculates the measure of merit to be optimized from a set
    of parameters.

    Parameters
    -------
    x : list
        A list of parameters whose order matches what was defined in 
        the initial guess vector (x0)

    Returns
    -------
    out : float
        The value of the transportation cost calculated from given parameters
    '''
    # print("ITERATION --")

    L, B, D, T, Cb = x
    # print(f"Length (L) after optimization: {L} [m]")
    # print(f"Breadth (B) after optimization: {B} [m]")
    # print(f"Depth (D) after optimization: {D} [m]")
    # print(f"Draught (T) after optimization: {T} [m]")
    # print(f"Block Coefficient (Cb) after optimization: {Cb}")

    ##########################################################################
    # Shared Variables
    ##########################################################################
    power = get_power(L, B, D, T, Cb)  # in Kilo Watts
    gross_tonnage = get_gross_tonnage(L, B, D)

    ##########################################################################
    # Capital Cost
    ##########################################################################
    outfit_weight = get_outfit_weight(L, B, D)  # in tons
    steel_weight = get_steel_weight(B, T, D, L, Cb)  # in tons
    machinery_weight = get_machinery_weight(power, 550)
    lightship_weight = get_lightship_weight(
        steel_weight, outfit_weight, machinery_weight)
    ship_cost = get_ship_cost(
        steel_weight, outfit_weight, Cb, power)

    ##########################################################################
    # Voyage Cost
    ##########################################################################
    fuel_cost_per_roundtrip = get_fuel_cost_per_roundtrip(power)
    port_cost_per_roundtrip = get_port_cost_per_roundtrip(gross_tonnage)
    annual_voyage_cost = (fuel_cost_per_roundtrip +
                          port_cost_per_roundtrip)*round_trips_per_year

    ##########################################################################
    # Annual Cost
    ##########################################################################
    annual_cost = ship_cost + annual_voyage_cost

    ##########################################################################
    # Printing Values
    ##########################################################################
    # print("----Optimization function main costs----")
    # print(f"Power: {power}")
    # print(f"Gross Tonnage: {gross_tonnage}")
    # print(f"Fuel Cost per Roundtrip: {fuel_cost_per_roundtrip}")
    # print(f"Port Cost per Roundtrip: {port_cost_per_roundtrip}")
    # print(f"Annual Voyage Cost: {annual_voyage_cost}")
    # print(f"Annual Cost: {annual_cost}")
    # print("END ITERATION -- \n")
    return annual_voyage_cost
