import numpy as np


def auc(y, s):
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    # average ties
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    r = (np.bincount(inv, r) / cnt)[inv]
    p = y > 0.5; n1, n0 = p.sum(), (~p).sum()
    return (r[p].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


