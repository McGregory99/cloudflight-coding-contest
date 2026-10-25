"""usage: b_train.py data.npz out.pt [epochs]"""
import sys, numpy as np, torch, torch.nn.functional as F
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from b_net import Net
torch.set_num_threads(2); torch.manual_seed(0); np.random.seed(0)


def auc(y, s):
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    # average ties
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    r = (np.bincount(inv, r) / cnt)[inv]
    p = y > 0.5; n1, n0 = p.sum(), (~p).sum()
    return (r[p].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


d = np.load(sys.argv[1]); X, W, T, Z, B = d["X"], d["W"], d["T"], d["Z"], d["bare"]
gi, bi = np.where(~B)[0], np.where(B)[0]
va = np.concatenate([gi[int(len(gi) * .9):], bi[int(len(bi) * .9):]]); tr = np.concatenate([gi[:int(len(gi) * .9)], bi[:int(len(bi) * .9)]])
print("train", len(tr), "val", len(va), "pos win", W.mean(), flush=True)
Xt, Wt, Tt, Zt = (torch.from_numpy(a) for a in (X, W, T, Z))
net = Net(); opt = torch.optim.Adam(net.parameters(), 1e-3); E = int(sys.argv[3]) if len(sys.argv) > 3 else 10
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, E * (len(tr) // 256 + 1))


def evaluate():
    net.eval()
    with torch.no_grad():
        h = torch.cat([net.heads(Xt[va[i:i + 2048]]) for i in range(0, len(va), 2048)]).numpy()
    net.train()
    ww, tt, zz = W[va], T[va], Z[va]
    return auc(ww, h[:, 0]), auc(tt, h[:, 1]), float(np.mean((np.tanh(h[:, 2]) - zz) ** 2)), \
        auc(ww[B[va]], h[B[va], 0]) if (ww[B[va]] > 0).any() else float("nan")


for ep in range(E):
    p = np.random.permutation(tr); tot = 0
    for i in range(0, len(p), 256):
        idx = torch.from_numpy(p[i:i + 256]); x = Xt[idx]
        flip = torch.rand(len(idx)) < 0.5
        x = torch.where(flip[:, None, None, None], x.flip(3), x)
        h = net.heads(x)
        loss = F.binary_cross_entropy_with_logits(h[:, 0], Wt[idx]) + F.binary_cross_entropy_with_logits(h[:, 1], Tt[idx]) \
            + F.mse_loss(torch.tanh(h[:, 2]), Zt[idx])
        opt.zero_grad(); loss.backward(); opt.step(); sched.step(); tot += loss.item() * len(idx)
    print("ep", ep, "loss %.4f" % (tot / len(p)), "val AUC win %.4f thr %.4f zmse %.4f bareAUCwin %.4f" % evaluate(), flush=True)
torch.save(net.state_dict(), sys.argv[2])
