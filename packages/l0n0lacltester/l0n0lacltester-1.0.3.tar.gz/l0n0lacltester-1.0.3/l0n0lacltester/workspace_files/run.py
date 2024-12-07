import sys
import numpy as np
import l0n0lacltester as tester
from op_args import AscendCOpArgs
if sys.argv[1] == 'cpu' or sys.argv[1] == 'sim':
    from op_cpu import AscendCOp
else:
    from op_npu import AscendCOp