from voyage_model.constants import dolar_to_euro


def get_ship_cost(steel_weight, outfit_weight, Cb,  power):
    hull_cost = 3.167*(steel_weight**0.8802) * (Cb**0.2217)
    equipment_cost = 14.77*(outfit_weight**0.9313)
    machinery_cost = 12.507*(power**0.647)  # Diesel 4 stroke engine
    total_cost = 1.1*(hull_cost + equipment_cost +
                      machinery_cost)  # 1.1 as safe margin
    correction_factor = 4000
    return dolar_to_euro(total_cost)*correction_factor
