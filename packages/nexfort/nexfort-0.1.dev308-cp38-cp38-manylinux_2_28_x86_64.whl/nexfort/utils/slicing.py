

def only_keep_last_dim(x):
    dim = x.dim()
    if (dim <= 1):
        return x
    indices = ((0,) * (dim - 1))
    return x[indices]

def only_keep_last_element(x):
    dim = x.dim()
    if (dim <= 0):
        return x
    indices = ((0,) * dim)
    return x[indices]
