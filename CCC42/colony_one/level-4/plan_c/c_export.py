"""usage: c_export.py CKPT.pt OUT.onnx"""
import sys, subprocess, torch, onnx
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from c_net import Net
ck, out = sys.argv[1], sys.argv[2]
net = Net()
if ck != "zero":
    net.load_state_dict(torch.load(ck, map_location='cpu'))
net.eval()
tmp = out + ".raw"
torch.onnx.export(net, torch.zeros(2, 16, 8, 8), tmp, opset_version=17, dynamo=False, input_names=["observation"],
                  output_names=["policy", "value"], dynamic_axes={"observation": {0: "batch"}, "policy": {0: "batch"}, "value": {0: "batch"}})
import onnx
from onnx import numpy_helper
m = onnx.load(tmp); g = m.graph; keep = []
for n in g.node:
    if n.op_type == "Constant":
        g.initializer.append(numpy_helper.from_array(numpy_helper.to_array(n.attribute[0].t), n.output[0]))
    else: keep.append(n)
del g.node[:]; g.node.extend(keep)
m.ir_version = 8
d = g.output[0].type.tensor_type.shape.dim[1]; d.ClearField('dim_param'); d.dim_value = 4096
onnx.checker.check_model(m); onnx.save(m, out)
import os; os.remove(tmp)
print("ops:", sorted({n.op_type for n in m.graph.node}), os.path.getsize(out))
