import sys, onnx
from onnx import numpy_helper
m = onnx.load(sys.argv[1]); g = m.graph; keep = []
for n in g.node:
    if n.op_type == "Constant":
        t = numpy_helper.to_array(n.attribute[0].t); g.initializer.append(numpy_helper.from_array(t, n.output[0]))
    else: keep.append(n)
del g.node[:]; g.node.extend(keep); onnx.checker.check_model(m); onnx.save(m, sys.argv[2])
