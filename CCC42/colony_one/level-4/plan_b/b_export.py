import sys, numpy as np, torch
sys.path.insert(0, "."); from b_net import Net, export
from b_train_auc import auc
n = Net(); n.load_state_dict(torch.load("b_net.pt")); n.eval()
d = np.load("b_real.npz")
with torch.no_grad(): h = n.heads(torch.from_numpy(d["X"])).numpy()
sg = lambda x: 1 / (1 + np.exp(-x))
print("REAL win AUC %.4f thr AUC %.4f" % (auc(d["W"], h[:, 0]), auc(d["T"], h[:, 1])), "win=1 n", int(d["W"].sum()))
print("mean sigmoid(win) on win_now=1: %.3f, on 0: %.3f; thr on thr=1: %.3f" % (sg(h[d["W"] > 0, 0]).mean(), sg(h[d["W"] == 0, 0]).mean(), sg(h[d["T"] > 0, 1]).mean()))
for name, abc in {"b1": (3, 1, .5), "b2": (4, 2, 1), "b3": (2, 1, 1), "b4": (3, 1, 0)}.items(): export(n, name + ".onnx", *abc)
