def get_KB(T): return 0.53*T


def get_BMt(Cb, B, T):
    return (0.085*Cb - 0.002)*(B ** 2)/(T+Cb)


def get_KG(D): return 1 + 0.52*D


def get_GMt(T, Cb, B, D):
    return get_KB(T) + get_BMt(Cb, B, T) - get_KG(D)
