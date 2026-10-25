import sys, numpy as np, onnxruntime as ort, torch
sys.path.insert(0, "."); from b_net import Net, export
n = Net(); export(n, "/private/tmp/ccc_arch/b_zero.onnx", 0, 0, 0)
X = np.load("/private/tmp/ccc_arch/b_test.npz")["X"]
A = ort.InferenceSession("../model.onnx"); B = ort.InferenceSession("/private/tmp/ccc_arch/b_zero.onnx")
pa, va = A.run(None, {A.get_inputs()[0].name: X}); pb, vb = B.run(None, {"observation": X})
print(np.abs(pa - pb).max(), np.abs(va - vb).max(), vb.shape, [o.shape for o in B.get_outputs()])
