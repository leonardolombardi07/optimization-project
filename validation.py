from numerical_model.propulsion import get_power
from numerical_model.volumes import get_gross_tonnage, get_height_of_superstructure
from numerical_model.weights import get_displacement, get_outfit_weight, get_steel_weight, get_machinery_weight, get_lightship_weight
from numerical_model.costs import get_ship_cost
from voyage_model.costs import get_fuel_cost_per_roundtrip, get_port_cost_per_roundtrip


def compare_ship_model_to_database(ship, database_ship_results):
    lw, power, ship_cost, GT = get_ship_model_results(ship)
    db_lw, db_power, db_ship_cost, db_GT = database_ship_results

    def get_discrepancy(value, reference_value):
        return 100*abs(value - reference_value) / reference_value

    def print_values(title, ship_model_value, db_value):
        print(title)
        print(f"Ship Model: {round(ship_model_value, 2)}")
        print(f"Database: {round(db_value, 2)}")
        print(
            f"Percentual Discrepancy: {round(get_discrepancy(ship_model_value, db_value), 2)}")
        print("\n")

    # ---- Lightship Weight ----
    print_values("---- Lightship Weight ----", lw, db_lw)
    print_values("---- Propulsion (Power) ----", power, db_power)
    print_values("---- Ship Building Cost ----", ship_cost, db_ship_cost)
    print_values("---- Gross Tonnage ----", GT, db_GT)


def get_ship_model_results(ship):
    L, B, T, D, Cb = ship

    # ---- Propulsion and Eletrical Power Generation ----
    power = get_power(L, B, D, T, Cb)
    print(f"Power: {power}")

    # ---- Gross Tonnage ----
    GT = get_gross_tonnage(L, B, D)
    print(f"Gross Tonnage: {GT}")

    # Displacement
    displacement = get_displacement(L, B, T, Cb)
    print(f"Displacement: {displacement}")

    # Height of superstructure
    Hs = get_height_of_superstructure(L, B)
    print(f"Height of Superstructure: {Hs}")

    # ---- Lightship Weight ----
    outfit_weight, steel_weight, machinery_weight = get_outfit_weight(
        L, B, D), get_steel_weight(B, T, D, L, Cb), get_machinery_weight(power, 600)
    # print(f"Outfit Weight: {outfit_weight}$")
    # print(f"Steel Weight: {steel_weight}$")
    # print(f"Steel Weight: {machinery_weight}$")
    lightship_weight = get_lightship_weight(
        steel_weight, outfit_weight, machinery_weight)
    print(f"Lightship Weight: {lightship_weight}")

    # ---- Ship Building Cost ----
    ship_cost = get_ship_cost(steel_weight, outfit_weight, Cb, power)
    # print(f"Ship Building Cost: {ship_cost}$")

    # ---- Voyage Model ----
    fuel_cost_per_round_trip = get_fuel_cost_per_roundtrip(power)
    port_costs_per_round_trip = get_port_cost_per_roundtrip(GT)
    # print("---- Voyage Model ----")
    # print(f"Fuel cost per round trip: {fuel_cost_per_round_trip}")
    # print(f"Port costs per round trip: {port_costs_per_round_trip}")
    # print("\n")
    return lightship_weight, power, ship_cost, GT


# ship = [L, B, T, D, Cb]
# database_results = [lw, power, cost, GT]

mein_schiff_two = [293, 42, 8.1, 11.2, 0.75]
db_mein_schiff_two = [68767, 44000, (500*(10 ** 6)), 111554]

AIDAperla = [294, 37.65, 8.25, 14.13, 0.8]
db_AIDAperla = [65682, 46800, (550*(10 ** 6)), 125572]


print("Mein Schiff Two")
compare_ship_model_to_database(mein_schiff_two, db_mein_schiff_two)
print("\n")


print("AIDAperla")
compare_ship_model_to_database(AIDAperla, db_AIDAperla)
print("\n")


optimized_gross_tonnage_ship = [222.2,	34.3,	10.5,	7.5,	0.6]
optimized_power_ship = [246.45,	30.5,	10,	7,	0.55]
optimized_lightship_weight_ship = [220.3,	30,	10,	7,	0.55]
optimized_annual_voyage_ship_ship = [225.875,	30,	11.8,	8.2,	0.68]
ships = [optimized_gross_tonnage_ship, optimized_power_ship, optimized_lightship_weight_ship,
         optimized_annual_voyage_ship_ship]

for index, ship in enumerate(ships):
    print(f"Optimized Ship number {index+1}")
    compare_ship_model_to_database(ship, [1, 2, 3, 4])
    print("\n")
