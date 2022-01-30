from voyage_model.constants import num_of_pax, num_of_crew


def get_cargo_volume():
    standard_cabin_volume = 16 * 2.5  # cubic meters
    family_cabin_volume = 25 * 2.5  # cubic meters
    suite_cabin_volume = 45 * 2.5  # cubic meters

    number_of_standard_cabins = 0.9*(num_of_pax / 2) + num_of_crew
    number_of_family_cabins = 0.06*num_of_pax
    number_of_suit_cabins = 0.04*num_of_pax

    return (standard_cabin_volume * number_of_standard_cabins +
            family_cabin_volume * number_of_family_cabins +
            suite_cabin_volume * number_of_suit_cabins)  # in cubic meters
