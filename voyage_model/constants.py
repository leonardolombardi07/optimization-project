# From Economical Analysis, these define our goals
round_trip_miles = 1847  # Lisbon to Funchal to Ponta Delgada to Lisbon again
round_trips_per_year = 52
num_of_pax = 2500  # per roundtrip
num_of_crew = 0.39*num_of_pax  # 0.39 comes from database, per roundtrip
num_of_pax_plus_crew = num_of_pax + num_of_crew
Vk = 17  # Service speed, in knots
V = 0.5144*Vk  # Service speed, in meters per second

# Days on sea and on each port per roundtrip
num_of_days_per_round_trip = round(round_trips_per_year / 365)
num_of_days_on_sea = round_trip_miles/(24*Vk)
num_of_days_on_funchal = (5/24)  # 5 hours
num_of_days_on_ponta_delgada = (5/24)  # 5 hours
num_of_days_on_lisbon = (num_of_days_per_round_trip - num_of_days_on_sea -
                         num_of_days_on_funchal -
                         num_of_days_on_ponta_delgada)  # Lisbon is where maintenance is done


# Fuel and Energy Consumption
fuel_price = 595 * 0.88 / 1000  # Euros per Kg
num_of_engines = 4
E_fuel = 46*(10**3)  # Kilo Joules/ Kg
engine_efficiency = 0.40

# Passenger Handling
lisbon_start_embarking, lisbon_start_debarking = 0.8, 0
funchal_embarking, funchal_debarking = 0.0031, 0.0037
ponta_delgada_embarking, ponta_delgada_debarking = 0.0061, 0.0062
lisbon_end_embarking, lisbon_end_debarking = 0, 0.7993


def dolar_to_euro(dolars):
    return 0.88*dolars
