from physical_constants import p
from voyage_model.constants import num_of_engines, num_of_crew, num_of_pax, num_of_pax_plus_crew
from numerical_model.volumes import get_length_of_deck, get_height_of_superstructure


def get_displacement(L, B, T, Cb):
    return p*L*B*T*Cb


def get_lightship_weight(steel_weight, outfit_weight, machinery_weight):
    correction_factor = 1.6
    # in tons
    return correction_factor*(steel_weight + outfit_weight + machinery_weight)


def get_DWT(displacement, lightship_weight):
    return displacement - lightship_weight


def get_extra_DWT(machinery_weight):
    crew_weight = num_of_crew * 500  # in Kg
    passenger_weight = num_of_pax*200  # in Kg
    # The rest is produced in ship
    fresh_water_weight = 0.1*200*num_of_pax_plus_crew  # in Kg
    lube_oil_weight = 13*num_of_engines * 0.91*1000  # in Kg
    spare_parts_of_engine_weight = 0.03*machinery_weight
    return (crew_weight + passenger_weight + fresh_water_weight + lube_oil_weight+spare_parts_of_engine_weight)


def get_steel_weight(B, T, D, L, Cb):
    area_1 = get_length_times_height_of_full_width_erections(L, B)
    area_2 = get_length_times_height_of_deck_house_operations(L, B)
    E = L*(B + T) + 0.85*L*(D - T) + 0.85 * area_1 + 0.75 * area_2
    k_cruise = 0.0375  # Constant considering the type of ship we use
    return k_cruise*(E**(1.36))*(1 + 0.5*(Cb - 0.7))  # in tons


def get_outfit_weight(L, B, D):
    # Frp, statistical analysis regression (d'Almeida, 2009)
    # We consider the same parameters as container carries, as cruise ships are similar in hull form
    k1, k2 = 0.1156, 0.85
    return k1*((L*B*D)*k2)  # in tons


def get_length_times_height_of_full_width_erections(L, B):
    # Length of cargo area, considering the colision bulkhead
    full_width_erections_length = get_length_of_deck(L)
    full_width_erections_height = get_height_of_superstructure(L, B)
    return full_width_erections_length * full_width_erections_height


def get_machinery_weight(power, rpm):
    return 9.38*(power/rpm)**0.84 + 0.65*(power**0.17)  # in tons


def get_length_times_height_of_deck_house_operations(L, B):
    # In our case it will be the same as the length_times_height_of_full_width_erections
    return get_length_times_height_of_full_width_erections(L, B)
