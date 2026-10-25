"""usage: c_train.py OUT.pt EPOCHS POLICY_ONLY(0/1) shard_glob [shard_glob ...]"""
import sys, glob, time, numpy as np, torch, torch.nn.functional as F
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from c_net import Net
torch.set_num_threads(2); torch.manual_seed(0); np.random.seed(0)
out, epochs, pol_only = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
files = sorted(f for g in sys.argv[4:] for f in glob.glob(g))
tr_f = [f for i, f in enumerate(files) if i % 10 != 9]; va_f = [f for i, f in enumerate(files) if i % 10 == 9] or files[-1:]
def load(fs):
    d = [np.load(f) for f in fs]
    return (np.concatenate([x["planes"] for x in d]), np.concatenate([x["visits"] for x in d]),
            np.concatenate([x["legal"] for x in d]), np.concatenate([x["z"] for x in d]), np.concatenate([x["q"] for x in d]))
def batch(D, idx):
    pl, vi, le, z, q = D
    x = torch.from_numpy(pl[idx].astype(np.float32))
    v = torch.from_numpy(vi[idx].astype(np.float32)); v = v / v.sum(1, keepdim=True)
    m = torch.from_numpy(np.unpackbits(le[idx], axis=1).astype(bool))
    return x, v, m, torch.from_numpy(0.5 * z[idx] + 0.5 * q[idx])
TR, VA = load(tr_f), load(va_f)
print("train positions", len(TR[3]), "val", len(VA[3]), "files", len(files), flush=True)
net = Net(); params = [p for n, p in net.named_parameters()]
opt = torch.optim.Adam(params, lr=1e-3, weight_decay=1e-5)
N = len(TR[3]); bs = 256; steps = epochs * (N // bs); sched = torch.optim.lr_scheduler.OneCycleLR(opt, 2e-3, total_steps=steps)
def losses(x, v, m, t):
    lg, val = net(x)
    lg = lg.masked_fill(~m, -1e9)
    lp = -(v * F.log_softmax(lg, 1).masked_fill(~m, 0)).sum(1).mean()
    lv = F.mse_loss(val, t)
    return lp, lv
def evaluate():
    net.eval(); a = b = 0; n = 0
    with torch.no_grad():
        for i in range(0, len(VA[3]), 1024):
            lp, lv = losses(*batch(VA, np.arange(i, min(i + 1024, len(VA[3])))))
            k = min(1024, len(VA[3]) - i); a += lp.item() * k; b += lv.item() * k; n += k
    net.train(); return a / n, b / n
print("val before: pol %.4f val %.4f" % evaluate(), flush=True)
t0 = time.time(); step = 0
for ep in range(epochs):
    perm = np.random.permutation(N); lp_s = lv_s = 0; c = 0
    for i in range(0, N - bs + 1, bs):
        lp, lv = losses(*batch(TR, np.sort(perm[i:i + bs])))
        loss = lp if pol_only else lp + lv
        opt.zero_grad(); loss.backward(); opt.step(); sched.step(); step += 1
        lp_s += lp.item(); lv_s += lv.item(); c += 1
    print("epoch %d train pol %.4f val %.4f | val pol %.4f val %.4f | %.0fs" % ((ep, lp_s / c, lv_s / c) + evaluate() + (time.time() - t0,)), flush=True)
torch.save(net.state_dict(), out)
