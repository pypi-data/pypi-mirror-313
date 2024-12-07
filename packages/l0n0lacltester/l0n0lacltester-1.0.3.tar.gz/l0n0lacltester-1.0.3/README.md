# 1 功能描述
由于在ascendc算子开发过程中运行算子比较复杂，为了简化算子的运行，将运行算子变成可以用python直接调用的函数。所以编写了此代码。

# 2 安装
```
pip install l0n0lacltester
```

# 3 运行算子实例
## 3.1 先切换到cann环境,比如我的环境是:
```
source /home/HwHiAiUser/Ascend/ascend-toolkit/set_env.sh
```

# 4 创建测试用例工程
## 4.1 命令行参数
```
l0n0lacltester -h
usage: l0n0lacltester [-h] op_path test_path

创建测试工程

positional arguments:
  op_path     ascendc算子目录
  test_path   测试工程目录

optional arguments:
  -h, --help  show this help message and exit
```
## 4.2 举例
```
l0n0lacltester 算子目录 测试工程目录
```
### 4.2.1 工程结构:
```
cmake
    - cpu_lib.cmake
    - npu_lib.cmake
include
    - *.h
.gitignore
CMakeLists.txt
gen_code.py
run.py
run.sh    
tiling_context.cpp
```
上面需要关注的只有gen_code.py 与 run.py

### 4.2.2 算子工程设置
### 4.2.2.1 设置tiling namespace
默认情况下的optiling如下
```c++
namespace optiling {
static ge::graphStatus TilingFunc(gert::TilingContext *context) {
  return ge::GRAPH_SUCCESS;
}
}
```
由于本工具是用python的re模块正则表达式匹配的，所以需要在
在namespace末尾添加 `// namespace optiling`
```c++
namespace optiling {
static ge::graphStatus TilingFunc(gert::TilingContext *context) {
  return ge::GRAPH_SUCCESS;
}
} // namespace optiling
```

## 4.3 gen_code.py
```python
import os
from l0n0lacltester.gen_cpu_call_code import generate_all_codes
current_path = os.path.split(__file__)[0]
# 比如['/mnt/code/a','/mnt/code/b']
include_dirs=[
   
]
# enum class KernelMode {
#     MIX_MODE = 0, # 融合模式，启用向量运算单元(aiv)与矩阵运算单元(aic)。一个block一个aic, n个aiv(n >= 1)。
#     AIC_MODE, # 仅使用矩阵运算单元(aic)。一个block仅包含一个aic。
#     AIV_MODE, # 仅使用向量运算单元(aiv)。一个block仅包含一个aiv。
#     MIX_AIC_1_1, # 矩阵运算单元(aic)与向量运算单元(aiv) 1:1合并为一个block。 一个block包含一个aiv一个aic。
# };
CPU_KERNEL_MODE='KernelMode::AIV_MODE'
generate_all_codes(f'算子目录绝对地址', '.', include_dirs, CPU_KERNEL_MODE)
    
```
需要关注的是include_dirs 与generate_all_codes的第一个参数
### 4.3.1 include_dirs
如果算子工程使用了算子工程目录之外的`.h`文件。则需要将该include目录`绝对地址`写到include_dirs中

比如
```python
include_dirs=[
 '/mnt/code/a',
 '/mnt/code/b'  
]
```
### 4.3.2 CPU_KERNEL_MODE
仅在cpu模式下情况下起效
可选项有
```c++
enum class KernelMode {
    MIX_MODE = 0, # 融合模式，启用向量运算单元(aiv)与矩阵运算单元(aic)。一个block一个aic, n个aiv(n >= 1)。
    AIC_MODE, # 仅使用矩阵运算单元(aic)。一个block仅包含一个aic。
    AIV_MODE, # 仅使用向量运算单元(aiv)。一个block仅包含一个aiv。
    MIX_AIC_1_1, # 矩阵运算单元(aic)与向量运算单元(aiv) 1:1合并为一个block。 一个block包含一个aiv一个aic。
};
```

### 4.3.3 generate_all_codes
generate_all_codes用于生成cpu|sim运行模式所需要的代码。

generate_all_codes的第一个参数是算子工程的`绝对地址`

比如
```python
generate_all_codes(f'算子目录绝对地址', '.', include_dirs, CPU_KERNEL_MODE)
```
current_path表示`gen_code.py`所在的目录

## 4.4 run.py
初始情况下
```python
import sys
import numpy as np
import l0n0lacltester as tester
from op_args import AscendCOpArgs
if sys.argv[1] == 'cpu' or sys.argv[1] == 'sim':
    from op_cpu import AscendCOp
else:
    from op_npu import AscendCOp
```
### 4.4.1 `AscendCOp` 可以用于调用算子
```python
b = 8
c = 32
ignore_index = -100
reduction='sum'
x_shape = [b, c]
target_shape = [b]
weight_shape = [c]
input_x = np.random.uniform(-5, 5, x_shape).astype(np.float32)
input_target = np.random.uniform(0, 31, target_shape).astype(np.int32)
input_weight = np.random.uniform(0, 1, weight_shape).astype(np.float32)
y = np.random.uniform(0, 1, [1]).astype(np.float32)
op = AscendCOp(reduction, ignore_index)
op(input_x, input_target, input_weight, y)
print('y = ', y)
```
### 4.4.2 `AscendCOpArgs` 用于保存参数,并且可以用于调用`AscendCOp`
基本范式为:
```python
# 创建测试用例
args = AscendCOpArgs(‘保存文件.json’)
# 尝试读取 '保存文件.json'
if not args.try_load():
  # 生成测试数据
  pass
# 调用算子
args.run_op(AscendCOp)
# 检测精度
if 精度检测通过:
  tester.print_green("成功")
  # 移除存储的测试数据
  args.remove_record()
else:
  tester.print_red("失败")
  # 将测试数据保存到 '保存文件.json'
  args.save()
```
举例
```python
import sys
import torch
import numpy as np
import l0n0lacltester as tester
from op_args import AscendCOpArgs
if sys.argv[1] == 'cpu' or sys.argv[1] == 'sim':
    from op_cpu import AscendCOp
else:
    from op_npu import AscendCOp
args = AscendCOpArgs(name)
if not args.try_load():
    input_x = np.random.uniform(-5, 5, x_shape)
    golden = 标杆算子(input_x)
    args.set_x(input_x)
    args.set_golden(golden)
args.run_op(AscendCOp)
output = torch.tensor(args.get_y())
golden = torch.tensor(args.get_golden())
if torch.allclose(output, golden, 1e-4, 1e-4):
    tester.print_green('成功')
    args.remove_record()
else:
    tester.print_red("失败")
    args.save()
```

## 4.3 关于COMMON_TILING宏定义
`COMMON_TILING`宏定义是用于在tiling结构定义时，复用某些结构用的

范式为:
```c++
#define COMMON_TILING_XXX(arg) \
  ...
// END COMMON_TILING_XXX
```
* 注意 `// END COMMON_TILING_XXX` 是必须的。用于正则表达式匹配

比如我有一个关于`tiling`的宏定义如下
```c++
#define COMMON_TILING_FILED_DEF(prefix)                                        \
  TILING_DATA_FIELD_DEF(int64_t, prefix##TileLength);                          \
  TILING_DATA_FIELD_DEF(int64_t, prefix##FormerNum);                           \
  TILING_DATA_FIELD_DEF(int64_t, prefix##FormerLength);                        \
  TILING_DATA_FIELD_DEF(int64_t, prefix##FormerFinalCalcCount);                \
  TILING_DATA_FIELD_DEF(int64_t, prefix##TailLength);                          \
  TILING_DATA_FIELD_DEF(int64_t, prefix##TailFinalCalcCount);                  \
  TILING_DATA_FIELD_DEF(int64_t, prefix##FinalKernelFinalCalcCount);           \
  TILING_DATA_FIELD_DEF(int64_t, prefix##KernelCount);
// END COMMON_TILING_FILED_DEF                     
```
tiling.h就可以使用它了
```c++
#include "register/tilingdata_base.h"
#include "tiling_defines.h"
namespace optiling {
BEGIN_TILING_DATA_DEF(NLLLossTilingData)
  TILING_DATA_FIELD_DEF(uint64_t, b);
  TILING_DATA_FIELD_DEF(uint64_t, c);
  TILING_DATA_FIELD_DEF(uint64_t, d);
  TILING_DATA_FIELD_DEF(int64_t, reduction);
  TILING_DATA_FIELD_DEF(int64_t, ignore_index);
  COMMON_TILING_FILED_DEF(b); 
  TILING_DATA_FIELD_DEF(int32_t, dimFlag);
END_TILING_DATA_DEF;

REGISTER_TILING_DATA_CLASS(NLLLoss, NLLLossTilingData)
} // namespace optiling

```
# 5 运行
```bash
# bash run.sh -h
run.sh [option]
-v 芯片型号(默认Ascend910B1)
-r 运行模式(cpu[默认]|sim|npu)
-n 对于cpu|sim模式不重新编译代码
-h 显示此帮助
```
实例

默认为 `Ascend910B1` `cpu` 模式
```
bash run.sh
```
```
bash run.sh -v Ascend910B1 -r cpu
```
