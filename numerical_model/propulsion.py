import numpy as np
from physical_constants import g, p, vk, get_froude_number
from voyage_model.constants import V, num_of_pax_plus_crew
from numerical_model.volumes import get_height_of_superstructure
from numerical_model.weights import get_displacement


def get_power(L, B, D, T, Cb):
    resistance = get_resistance(L, B, D, T, Cb)
    effective_power = resistance * V

    w = 0.55*Cb - 0.2
    t = 1.25*w
    Nh = (1-t)/(1-w)  # TODO: How to incorporate Diesel/Eletric power?
    # TODO: 0.7 depends on the propeller. maybe change later
    efficiency_denominator = 0.98*0.995*1.01*Nh*0.7
    propulsive_power = effective_power / (efficiency_denominator)

    # KW - TODO: get this from database automatically
    mean_of_power_per_person_ratio = 13.41
    mean_from_database_total_power = mean_of_power_per_person_ratio * \
        num_of_pax_plus_crew
    expected_entertainment_power = mean_from_database_total_power * 0.7

    total_power = propulsive_power + expected_entertainment_power
    correction_factor = 1.2
    return correction_factor * total_power  # in Kilo Watts


def get_resistance(L, B, D, T, Cb):
    # k
    k_denominator = ((L/B)**2) * np.sqrt(B/T)
    k = -0.095 + 25.6 * (Cb / k_denominator)

    # Cf
    Re = V*L / vk
    Cf = 0.075 / ((np.log(Re) - 2)**2)

    # DCf
    # According to ITTC, international towing ... conference
    Ks = 150 * (10**-6)
    DCf = (105*((Ks/L)**(1/3)) - 0.64)*(10**-3)  # Roughness of the hull

    # Caa
    At = (get_height_of_superstructure(L, B) + (D - T)) * \
        B  # Projected area of superstructure
    S = 1.025*L*(Cb*B + 1.7*T)
    Caa = 0.001*(At/S)

    Ct = (1 + k)*Cf + DCf + Caa

    # Rw
    Cp = 0.85  # Approximated as average from table
    froude_number = get_froude_number(V, L)
    # 1cb is the longitudinal position of thecentre of buoyancy forward of 0.5L as a percentage
    # of the waterline length L. LR
    lcb = (8.8 - 38.9*froude_number)/100
    alpha = 125.67*(B/L) - 162.25*(Cp**2) + 234.32 * \
        (Cp**3) + 0.155087*(lcb**3)
    c1 = (2223105*(B/L)**3.78613) * ((T/B)**1.07961) * \
        ((90 - alpha)**(-1.37565))
    # We assume the diamater of the bulbous head as equal to the draught T
    AB = np.pi*(T**2)/4
    hB = T/2
    c3_denominator = B*T * (0.56*np.sqrt(AB)) + T - hB - 0.25*np.sqrt(AB)
    c3 = 0.56*(AB**1.5) / c3_denominator
    c2 = np.exp(-1.89*np.sqrt(c3))
    lambda_ = 1.446*Cp - 0.03 * (L/B)

    m1 = 0.0140407*(L/T) - 1.75254*(get_displacement(L, B, T, Cb)**(1/3)) / \
        L - 4.793*(B/L) - 8.08*(Cp) + 13.87*(Cp**2)-6.984*(Cp**3)
    m2 = -1.694*(Cp**2)*np.exp(-0.1/froude_number**2)
    d = -0.9

    weight_of_ship = p*get_displacement(L, B, T, Cb)
    Rw = c1*c2*np.exp(m1*(froude_number**d) + m2 *
                      np.cos(lambda_*(froude_number**-2)))*weight_of_ship
    resistance = Ct*(1/2)*p*(V**2)*S + Rw
    return resistance
