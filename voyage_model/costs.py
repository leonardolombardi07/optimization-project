from .constants import *


def get_port_cost_per_roundtrip(gross_tonnage):
    lisbon_cost = get_lisbon_port_cost_per_roundtrip(gross_tonnage)
    funchal_cost = get_funchal_port_cost_per_roundtrip(gross_tonnage)
    ponta_delgada_cost = get_ponta_delgada_port_cost_per_roundtrip(
        gross_tonnage)
    return lisbon_cost + funchal_cost + ponta_delgada_cost


def get_fuel_cost_per_roundtrip(power):
    sea_day_daily_consumption = (power/(E_fuel*engine_efficiency))*(3600*24)
    sea_days_fuel_cost = sea_day_daily_consumption * fuel_price

    lisbon_port_daily_consumption = sea_day_daily_consumption * \
        0.1  # 10% of sea day consumption, less than others because some time without pax and crew
    funchal_port_daily_consumption = sea_day_daily_consumption * \
        0.3  # 30% of sea day consumption
    ponta_delgada_port_daily_consumption = sea_day_daily_consumption * \
        0.3  # 30% of sea day consumption

    sailing_fuel_cost = sea_days_fuel_cost * num_of_days_on_sea
    lisbon_fuel_cost = lisbon_port_daily_consumption * fuel_price * 2  # 2 days on port
    funchal_fuel_cost = funchal_port_daily_consumption * \
        fuel_price * (24/5)  # 5 hours on port
    ponta_delgada_fuel_cost = ponta_delgada_port_daily_consumption * \
        fuel_price * (24/5)  # 5 hours on port

    safe_margin = 1.05
    return safe_margin * (sailing_fuel_cost + lisbon_fuel_cost + funchal_fuel_cost + ponta_delgada_fuel_cost)


def get_lisbon_port_cost_per_roundtrip(gross_tonnage):
    def get_port_cost_per_stop(num_of_pax):
        terminal_use_fee = 3.9643 * num_of_pax
        luggage_fee = ((5*9.5950 + 2*9.6909) / (5+2))*num_of_pax
        x_ray_service = 2.0464*num_of_pax
        gangway = 90.95*1  # 1 day only
        removal_of_gangways = 90.95*1  # 1 day only
        port_fee_discount = 0.75  # We assume (53-100 stops/year)
        port_fee = 0.0766*gross_tonnage*port_fee_discount
        carbon_tariff_discount = 0.5  # Because our ship does turnaround trips
        carbon_tariff = 2 * num_of_pax*carbon_tariff_discount
        waste_fee = min(200, 0.009*gross_tonnage)
        return (terminal_use_fee + luggage_fee + x_ray_service + gangway + removal_of_gangways
                + port_fee + carbon_tariff + waste_fee)

    round_trip_start_cost = get_port_cost_per_stop(
        num_of_pax * lisbon_start_embarking)
    round_trip_end_cost = get_port_cost_per_stop(
        num_of_pax*lisbon_end_debarking)
    return round_trip_start_cost + round_trip_end_cost


def get_funchal_port_cost_per_roundtrip(gross_tonnage):
    PED = (funchal_embarking + funchal_debarking) * \
        num_of_pax  # Pax embarking or debarking
    PT = (lisbon_start_embarking - funchal_debarking) * \
        num_of_pax  # Pax in transit
    number_of_days_in_port = 1
    scaled_betweeen_june_and_august_discount = 0.25
    # Considering gross_tonnage >= 101.000
    scaled_between_september_and_may_discount = 0.7
    cumulative_port_fee_discount = 92.5  # Considering more than 60 scales per year
    port_use_fee_without_discount = 0.0641*gross_tonnage + \
        0.0306*gross_tonnage * (number_of_days_in_port-1)
    port_use_fee = port_use_fee_without_discount * scaled_betweeen_june_and_august_discount * \
        scaled_between_september_and_may_discount*cumulative_port_fee_discount

    terminal_use_fee = 50 + 6.08*PED + 2.46*PT + 0.5*(PED + PT)
    mooring_fee = 226*5  # Assuming 5 hours for embarking and debarking
    waste_fee = 60  # TODO: check this
    return port_use_fee + terminal_use_fee + mooring_fee + waste_fee


def get_ponta_delgada_port_cost_per_roundtrip(gross_tonnage):
    number_of_days_in_port = 1
    cruise_ship_discount = 0.7
    regular_ship_discount = 0.95  # We analyse the long run (+- 10 years)
    scaling_discount = 0.9  # We consider gross_tonnage > 250
    port_use_fee_without_discount = 0.0807*gross_tonnage + \
        0.0538*gross_tonnage * (number_of_days_in_port-1)
    port_use_fee = port_use_fee_without_discount * \
        cruise_ship_discount * regular_ship_discount * scaling_discount

    mooring_fee = 512.7983  # Assuming gross_tonnage > 40000
    other_fee = 0  # TODO: check this on document
    return port_use_fee + mooring_fee + other_fee
