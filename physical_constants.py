# Gravitational acceleration at the earth's surface, in meters per second squared
g = 9.805

# Sea water density, in kg per cubic meter
p = 1.025

# Kinematic viscosity of water, in millimeters squared per second
vk = 1.2 * (10**-6)


def get_froude_number(V, L):
    return V / ((g*L) ** 0.5)
