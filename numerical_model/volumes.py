from numerical_model.cargo import get_cargo_volume


def get_cubic_number(L, B, D):
    return L*B*D


def get_gross_tonnage(L, B, D):
    Cn = get_cubic_number(L, B, D)
    average_k_from_database = 0.80  # k = GT/ Cn
    return average_k_from_database * Cn


def get_length_of_deck(L):
    # We want the colision bulkhead to be as small as possible,
    # so we have more space for passengers. So we don't care about the
    # maximum distance, which should be min(0.08*L, 0.05*L+3)
    min_distance_between_colision_bulkhead_and_foward_perperpendicular = min(
        0.05*L, 10)
    return (L - min_distance_between_colision_bulkhead_and_foward_perperpendicular)


def get_height_of_superstructure(L, B):
    length_of_deck = get_length_of_deck(L)
    return get_cargo_volume() / (length_of_deck*B)
