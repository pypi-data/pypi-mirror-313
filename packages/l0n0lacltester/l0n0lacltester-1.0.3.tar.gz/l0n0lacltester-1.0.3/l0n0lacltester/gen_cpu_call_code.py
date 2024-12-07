import re
import os
import shutil
import argparse
from typing import List
from .utils import copy_files_from_directory
current_path = os.path.split(__file__)[0]


def extract_function(text, function_name):
    pattern = f'{function_name}[\s\S]*?\(([\s\S]*?)\)'
    match = re.search(pattern, text)
    if match:
        parameters = match.group(1).strip()
        parameters = ' '.join(parameters.split())
        return parameters


def gen_py_signature_and_call_parameters(
        fn_signature: str,
        dtype_list: List[str],
        value_list: List[str],
        ret_names: List[str],
        aclMemoryName: str):
    call_signature = fn_signature + ''
    mem_def = []
    call_param = []
    log_code = []
    for i, dtype in enumerate(dtype_list):
        param = value_list[i]
        if dtype == "GM_ADDR":
            size_name = f"{param}_memsize"
            mem_name = f"{param}_device"
            call_signature += f", int64_t {size_name}"
            mem_def.append(
                f'{aclMemoryName} {mem_name}({size_name}, {param});')
            call_param.append(f"{mem_name}.devPtr()")
            log_code.append(
                f'std::cout << "{size_name} = " << {size_name} << std::endl;')
        else:
            call_param.append(param)
    mem_def_str = '\n    '.join(mem_def)
    call_param_str = ', '.join(call_param)
    to_host_str = '\n    '.join(
        [f"{ret_name}_device.toHost();" for ret_name in ret_names])
    log_code_str = '\n    '.join(log_code)
    return call_signature, mem_def_str, call_param_str, to_host_str, log_code_str


def gen_call_lib(
        function_signature: str,
        dtype_list: List[str],
        value_list: List[str],
        function_name: str,
        ret_names: List[str]):
    shengming_signature = function_signature.replace("GM_ADDR", "uint8_t*")
    call_signature, mem_def_str, call_param_str, to_host_str, log_code_str = gen_py_signature_and_call_parameters(
        shengming_signature,
        dtype_list, value_list, ret_names, 'AclMemory')
    call_fun_def = f"""
#include "../include/all.h"
extern void do_{function_name}(uint32_t blockDim, void *stream, {shengming_signature});
extern "C" void run(uint32_t blockDim, {call_signature}){{
    AclEnv env;
    {log_code_str} 
    {mem_def_str}
    {{
        AclStream s;
        do_{function_name}(blockDim, s.stream, {call_param_str});
    }}
    {to_host_str}
}}
"""
    return call_fun_def


def gen_cpu_lib_code(
        fn_name: str,
        fn_signature: str,
        kernel_mode: str,
        dtype_list: List[str],
        value_list: List[str],
        ret_names: List[str]):
    '''
    enum class KernelMode {
        MIX_MODE = 0,
        AIC_MODE,
        AIV_MODE,
        MIX_AIC_1_1,
    };
    '''
    if kernel_mode == "0":
        kernel_mode = 'KernelMode::MIX_MODE'
    elif kernel_mode == "1":
        kernel_mode = 'KernelMode::AIC_MODE'
    elif kernel_mode == "2":
        kernel_mode = 'KernelMode::AIV_MODE'
    elif kernel_mode == "3":
        kernel_mode = 'KernelMode::MIX_AIC_1_1'
    call_signature, mem_def_str, call_param_str, to_host_str, log_code_str = gen_py_signature_and_call_parameters(
        fn_signature,
        dtype_list, value_list, ret_names, 'AclGmMemory')
    code = f'''
#include "tikicpulib.h"
#include "../include/AclGmMemory.h"
#include <iostream>
extern "C" __global__ __aicore__ void {fn_name} ({fn_signature});
extern "C" void run(uint32_t blockDim, {call_signature}){{
    {log_code_str}
    AscendC::SetKernelMode({kernel_mode});
    {mem_def_str}
    ICPU_RUN_KF({fn_name}, blockDim, {call_param_str});
    {to_host_str}
}}
'''
    return code


def get_dtype_value_list(function_signature: str):
    params_list = re.findall('\w+', function_signature)
    dtype_list = []
    value_list = []
    for i, v in enumerate(params_list):
        if i % 2 == 0:
            dtype_list.append(v)
        else:
            value_list.append(v)
    return dtype_list, value_list


def generate_do_function(
        function_signature: str,
        value_list: List[str],
        function_name: str):
    param_str = ', '.join(value_list)
    do_func_def = f"""
void do_{function_name}(uint32_t blockDim, void *stream, {function_signature}) {{
  {function_name}<<<blockDim, nullptr, stream>>>({param_str});
}}
"""
    return do_func_def


def replace_do_function(do_func_def: str, content: str, function_name: str):
    pattern = f'\s*?void do_{function_name}[\s\S]*?\}}'
    match = re.search(pattern, content)
    if match:
        return content.replace(match.group(0), do_func_def).strip()
    else:
        return content.strip() + '\n' + do_func_def


def remove_do_function(content: str, function_name: str):
    pattern = f'\s*?void do_{function_name}[\s\S]*?\}}'
    match = re.search(pattern, content)
    if match:
        return content.replace(match.group(0), '').strip()
    return content


def ctype_to_python_type(dtype: str):
    if dtype == "GM_ADDR":
        return "ctypes.c_void_p"
    elif dtype == "int64_t":
        return "ctypes.c_int64"
    elif dtype == "int32_t":
        return "ctypes.c_int32"
    elif dtype == "int16_t":
        return "ctypes.c_int16"
    elif dtype == "int8_t":
        return "ctypes.c_int8"
    elif dtype == "uint64_t":
        return "ctypes.c_uint64"
    elif dtype == "uint32_t":
        return "ctypes.c_uint32"
    elif dtype == "uint16_t":
        return "ctypes.c_uint16"
    elif dtype == "uint8_t":
        return "ctypes.c_uint8"
    elif dtype == "float":
        return "ctypes.c_float"
    elif dtype == "double":
        return "ctypes.c_double"
    elif dtype == "bool":
        return "ctypes.c_bool"


def gen_python_args(dtype_list, value_list):
    argtypes = ["ctypes.c_uint32"]
    finaltypes = []
    call_run_param = []
    call_run_final = []
    for i, dtype in enumerate(dtype_list):
        param = value_list[i]
        argtypes.append(ctype_to_python_type(dtype))
        if dtype == "GM_ADDR":
            finaltypes.append("ctypes.c_int64")
            if param == 'workspace':
                call_run_param.append('workspace')
                call_run_final.append('workspace_size')
            elif param == 'tiling':
                call_run_param.append(
                    f'self.context.raw_tiling_data.ctypes.data')
                call_run_final.append(
                    f'self.context.raw_tiling_data.size * self.context.raw_tiling_data.itemsize')
            else:
                call_run_param.append(f'{param}.ctypes.data')
                call_run_final.append(f'{param}.size * {param}.itemsize')
        else:
            call_run_param.append(param)

    return argtypes + finaltypes, call_run_param + call_run_final


def get_attr_dtype_value(op_path: str):
    tiling_path = f'{op_path}/op_host'
    dtype_list = []
    value_list = []
    for file in os.listdir(tiling_path):
        file_full_path = f'{tiling_path}/{file}'
        if not os.path.isfile(file_full_path):
            continue
        with open(file_full_path, 'r') as fp:
            file_data = fp.read()
        attr_list = re.findall(f'this->Attr[\s\S]+?;', file_data)
        for i, attr_str in enumerate(attr_list):
            pattern = 'Bool|Float|Int|String|ListBool|ListFloat|ListInt'
            match = re.search(pattern, attr_str)
            if match:
                dtype_list.append(match.group(0))
            match = re.search(f'this->Attr\(\"(.*?)\"\)', attr_str)
            if match:
                value_list.append(match.group(1))
        if len(attr_list) > 0:
            break

    for i, dtype in enumerate(dtype_list):
        if dtype == 'Bool':
            dtype_list[i] = 'bool'
        elif dtype == 'Float':
            dtype_list[i] = 'float'
        elif dtype == 'Int':
            dtype_list[i] = 'int'
        elif dtype == 'String':
            dtype_list[i] = 'str'
        elif dtype == 'ListBool':
            dtype_list[i] = 'List[bool]'
        elif dtype == 'ListFloat':
            dtype_list[i] = 'List[float]'
        elif dtype == 'ListInt':
            dtype_list[i] = 'List[int]'
    return dtype_list, value_list


def gen_python_run_args(dtype_list: List[str], value_list: List[str]):
    run_args: List[str] = []
    for i, dtype in enumerate(dtype_list):
        if dtype == 'GM_ADDR':
            arg = value_list[i]
            if arg != 'workspace' and arg != 'tiling':
                run_args.append(f'{arg}:np.ndarray')
        else:
            run_args.append(value_list[i])
    return run_args


def gen_python_attr_code(attr_dtype_list: List[str], attr_value_list: List[str]):
    attr_str = ''
    attr_set_code: List[str] = []
    for i, dtype in enumerate(attr_dtype_list):
        v = attr_value_list[i]
        if i != 0:
            attr_str += ', '
        attr_str += f'{v}:{dtype}'
        if dtype == 'bool':
            attr_set_code.append(f'self.context.set_attr_bool({i}, {v})')
        elif dtype == 'float':
            attr_set_code.append(f'self.context.set_attr_float({i}, {v})')
        elif dtype == 'int':
            attr_set_code.append(f'self.context.set_attr_int({i}, {v})')
        elif dtype == 'str':
            attr_set_code.append(f'self.context.set_attr_string({i}, {v})')
        elif dtype == 'List[bool]':
            attr_set_code.append(f'self.context.set_attr_list_bool({i}, {v})')
        elif dtype == 'List[float]':
            attr_set_code.append(f'self.context.set_attr_list_float({i}, {v})')
        elif dtype == 'List[int]':
            attr_set_code.append(f'self.context.set_attr_list_int({i}, {v})')
    return attr_str, attr_set_code


def gen_python_code(
        dtype_list: List[str],
        value_list: List[str],
        ret_names: List[str],
        attr_dtype_list: List[str],
        attr_value_list: List[str]):
    argtypes, call_run_param = gen_python_args(dtype_list, value_list)
    argtypes_str = ',\n    '.join(argtypes)
    run_args = gen_python_run_args(dtype_list, value_list)
    shape_code = []
    for arg in value_list:
        if arg != 'workspace' and arg != 'tiling':
            if arg in ret_names:
                shape_code.append(
                    f'self.context.push_output_shape({arg}.shape)')
                shape_code.append(
                    f'self.context.push_output_desc({arg}.dtype)')
            else:
                shape_code.append(
                    f'self.context.push_input_shape({arg}.shape)')
                shape_code.append(f'self.context.push_input_desc({arg}.dtype)')

    run_arg_str = ', '.join(run_args)
    run_call_str = ',\n        '.join(call_run_param)
    shape_code_str = ',\n        '.join(shape_code)
    attr_str, attr_set_code = gen_python_attr_code(
        attr_dtype_list, attr_value_list)
    attr_set_str = '\n        '.join(attr_set_code)
    code = f'''
import os
import ctypes
import numpy as np
from typing import List
from l0n0lacltester import TilingContext
current_file_path = os.path.split(__file__)[0]
lib_path = f"{{current_file_path}}/build/libascendc_kernels_bbit.so"
lib = ctypes.CDLL(lib_path)
lib.TilingFunc.argtypes = [ctypes.c_void_p]
lib.run.argtypes = [
    {argtypes_str}]

class AscendCOp:
    def __init__(self, {attr_str}):
        self.context = TilingContext(lib) 
        {attr_set_str}

    def __call__(self, {run_arg_str}):
        {shape_code_str}
        lib.TilingFunc(self.context.context_ptr)
        workspace_size = self.context.get_workspace_size()
        workspace = 0
        if workspace_size > 0:
            workspace = np.zeros(workspace_size, dtype=np.uint8)
            workspace = workspace.ctypes.data
        lib.run(self.context.get_block_dim(), {run_call_str})
'''
    return code


def get_kernel_file(op_path: str):
    kernel_path = f'{op_path}/op_kernel'
    for file in os.listdir(kernel_path):
        if os.path.splitext(file)[1] == '.cpp':
            return f'{kernel_path}/{file}'


def replace_tiling_define(name: str, target_args: List[str], include_dirs: List[str] = []):
    if include_dirs is None:
        return
    for base_path in include_dirs:
        base_path = base_path.strip()
        if len(base_path) == 0:
            continue
        for file in os.listdir(base_path):
            if not os.path.isfile(f'{base_path}/{file}'):
                continue
            with open(f'{base_path}/{file}') as fp:
                tiling_defines = fp.read()
            match = re.search(
                f'#define {name}[\s\S]+?END {name}', tiling_defines)
            if match is None:
                continue
            micro = match.group(0)
            args = []
            match = re.search(f'{name}\((.*)\)', tiling_defines)
            if match:
                args = match.group(1).split(',')
                args = [arg.strip() for arg in args]
            # 替换##target_args##
            for i, target_arg in enumerate(target_args):
                old_arg = args[i]
                micro = micro.replace(f'{old_arg}', target_arg)
                micro = micro.replace(f'##', '')
                micro = micro.replace(f'#{target_arg}', f'"{target_arg}"')
            fields = re.findall(f'TILING_DATA_FIELD_DEF.+?;', micro)
            return '\n'.join(fields)


def gen_tiling_code(op_path: str, include_dirs: List[str] = None):
    tiling_path = f'{op_path}/op_host'
    for file in os.listdir(tiling_path):
        file_full_path = f'{tiling_path}/{file}'
        if not os.path.isfile(file_full_path):
            continue
        with open(file_full_path, 'r') as fp:
            file_data = fp.read()
        match = re.search(
            'namespace optiling \{([\s\S]+)\} // namespace optiling', file_data)
        if match:
            tiling_function = match.group(1).replace(
                "static ge::graphStatus", "ge::graphStatus").strip()
        match = re.search(
            'BEGIN_TILING_DATA_DEF[\s\S]+?END_TILING_DATA_DEF;', file_data)
        if match:
            tiling_def = match.group(0)
            includes = []
            for include in re.findall('#include.*', file_data):
                if re.search('register/tilingdata_base', include):
                    continue
                includes.append(include)
            includes_str = '\n'.join(includes)
    cpu_code = f'''
{includes_str}
#include <iostream>
#include "include/tiling_context.h"
#include "include/tiling_data_base.h"
#include "graph/ge_error_codes.h"
{tiling_def}
extern "C" {{
{tiling_function}
}}
'''
    common_defs = re.findall(f'COMMON_TILING.+?;', tiling_def)
    while len(common_defs) > 0:
        for define in common_defs:
            match = re.search(f'(COMMON_TILING.+?)\((.+)\)', define)
            if match:
                define_name = match.group(1)
                args = match.group(2).split(',')
                args = [arg.strip() for arg in args]
                code = replace_tiling_define(
                    define_name, args, include_dirs)
                if code:
                    tiling_def = tiling_def.replace(define, code)
        common_defs = re.findall(f'COMMON_TILING.+?;', tiling_def)

    match = re.search('BEGIN_TILING_DATA_DEF\((.+)\)', tiling_def)
    class_name = match.group(1).strip()
    tiling_def_npu = tiling_def.replace(
        'BEGIN_TILING_DATA_DEF', 'BEGIN_KERNEL_TILING_DATA_DEF')
    tiling_def_npu = tiling_def_npu.replace(
        'TILING_DATA_FIELD_DEF', 'TILING_KERNEL_DATA_FIELD_DEF')
    tiling_def_npu = tiling_def_npu.replace(
        'TILING_DATA_FIELD_DEF_ARR', 'TILING_KERNEL_DATA_FIELD_DEF_ARR')
    tiling_def_npu = tiling_def_npu.replace(
        'END_TILING_DATA_DEF', 'END_KERNEL_TILING_DATA_DEF')

    tiling_load = tiling_def.replace(
        'TILING_DATA_FIELD_DEF(', f'TILING_LOAD_FIELD(helper, tiling_data, ')
    tiling_load = tiling_load.replace(
        'TILING_DATA_FIELD_DEF_ARR(', f'TILING_LOAD_ARR(helper, tiling_data, ')
    tiling_load = re.sub('BEGIN_TILING_DATA_DEF.*', '', tiling_load)
    tiling_load = re.sub('END_TILING_DATA_DEF.*', '', tiling_load).strip()

    npu_code = f'''
#include "include/tiling_data_kernel.h"
namespace AscendC{{
{tiling_def_npu}
inline __aicore__ void __load_tiling_data({class_name}& tiling_data, GM_ADDR tiling){{
    TilingDataHelper helper;
    helper.init(tiling);
    {tiling_load}
}}
#ifdef GET_TILING_DATA
#undef GET_TILING_DATA
#endif
#define GET_TILING_DATA(tiling_data, tiling) \\
    {class_name} tiling_data; \\
    __load_tiling_data(tiling_data, tiling);
}}
'''
    return cpu_code, npu_code


def get_op_io_name_list(op_path: str):
    tiling_path = f'{op_path}/op_host'
    for file in os.listdir(tiling_path):
        file_full_path = f'{tiling_path}/{file}'
        if not os.path.isfile(file_full_path):
            continue
        with open(file_full_path, 'r') as fp:
            file_data = fp.read()
        input_names: List[str] = re.findall(
            "this->Input\s*?\(([\s\S]*?)\)", file_data)
        output_names: List[str] = re.findall(
            "this->Output\s*?\(([\s\S]*?)\)", file_data)
        if len(input_names) + len(output_names) > 0:
            input_names = [name.replace('"', "").strip()
                           for name in input_names]
            output_names = [name.replace('"', "").strip()
                            for name in output_names]
            return input_names, output_names
    return [], []


def get_kernel_function_name(op_path: str):
    tiling_path = f'{op_path}/op_kernel'
    for file in os.listdir(tiling_path):
        file_full_path = f'{tiling_path}/{file}'
        if not os.path.isfile(file_full_path):
            continue
        with open(file_full_path, 'r') as fp:
            file_data = fp.read()
        match = re.search(
            'extern "C" __global__ __aicore__ void\s*?(\w+)', file_data)
        if match:
            return match.group(1).strip()


def get_op_name(op_path: str):
    tiling_path = f'{op_path}/op_host'
    for file in os.listdir(tiling_path):
        file_full_path = f'{tiling_path}/{file}'
        if not os.path.isfile(file_full_path):
            continue
        with open(file_full_path, 'r') as fp:
            file_data = fp.read()
        match = re.search('class\s+?(\w+?)\s+?:\s+?public\s+OpDef', file_data)
        if match:
            return match.group(1).strip()


def parse_args():
    parser = argparse.ArgumentParser(description="创建测试工程")
    parser.add_argument("op_path", type=str, help="ascendc算子目录")
    parser.add_argument("test_path", type=str, help="测试工程目录")
    return parser.parse_args()


def create_tiling(
        op_path: str, test_path: str,
        include_dirs: List[str] = None):
    tiling_file = f"{test_path}/tiling.cpp"
    tiling_npu_file = f"{test_path}/tiling_npu.h"
    tiling_cpu_code, tiling_npu_code = gen_tiling_code(
        op_path, include_dirs)
    with open(tiling_file, 'w') as fp:
        fp.write(tiling_cpu_code)
    with open(tiling_npu_file, 'w') as fp:
        fp.write(tiling_npu_code)


def create_cpu(
        test_path: str,
        output_names: List[str],
        dtype_list: List[str],
        value_list: List[str],
        fn_name: str,
        function_signature: str,
        content: str, CPU_KERNEL_MODE: str):
    if not os.path.exists(f'{test_path}/cpu'):
        os.mkdir(f'{test_path}/cpu')
    lib_file = f"{test_path}/cpu/lib.cpp"
    kernel_target_file = f"{test_path}/cpu/kernel.cpp"
    lib_code = gen_cpu_lib_code(
        fn_name, function_signature, CPU_KERNEL_MODE,
        dtype_list, value_list, output_names)
    with open(lib_file, 'w') as fp:
        fp.write(lib_code)
    with open(kernel_target_file, 'w') as fp:
        fp.write(f'''#include "../tiling_npu.h"\n{content}''')


def create_sim(
        test_path: str,
        output_names: List[str],
        dtype_list: List[str],
        value_list: List[str],
        fn_name: str,
        function_signature: str,
        content: str):
    if not os.path.exists(f'{test_path}/sim'):
        os.mkdir(f'{test_path}/sim')
    lib_file = f"{test_path}/sim/lib.cpp"
    kernel_target_file = f"{test_path}/sim/kernel.cpp"
    do_func_def = generate_do_function(
        function_signature, value_list, fn_name)
    generated_code = replace_do_function(do_func_def, content, fn_name)
    with open(kernel_target_file, 'w') as fp:
        fp.write(f'''#include "../tiling_npu.h"\n{generated_code}''')
    call_fun_def = gen_call_lib(
        function_signature, dtype_list, value_list, fn_name, output_names)
    with open(lib_file, 'w') as fp:
        fp.write(call_fun_def)


def gen_npu_python_code(
        op_path: str,
        input_names: List[str],
        output_names: List[str],
        dtype_list: List[str],
        value_list: List[str],
        attr_dtype_list: List[str],
        attr_value_list: List[str]):
    op_name = get_op_name(op_path)
    run_args: List[str] = gen_python_run_args(dtype_list, value_list)
    run_arg_str = ', '.join(run_args)
    attr_str = ''
    attr_call_args = []
    attr_set_code: List[str] = []
    for i, dtype in enumerate(attr_dtype_list):
        v = attr_value_list[i]
        if i != 0:
            attr_str += ', '
        attr_str += f'{v}:{dtype}'
        attr_call_args.append(f'self.{v}')
        if dtype == 'bool':
            attr_set_code.append(f'self.{v} = ctypes.c_bool({v})')
        elif dtype == 'float':
            attr_set_code.append(f'self.{v} = ctypes.c_float({v})')
        elif dtype == 'int':
            attr_set_code.append(f'self.{v} = ctypes.c_int({v})')
        elif dtype == 'str':
            attr_set_code.append(f'self.{v} = {v}.encode()')
        elif dtype == 'List[bool]':
            attr_set_code.append(
                f'self.{v} = AclArray(np.array({v}, dtype = np.bool_))')
        elif dtype == 'List[float]':
            attr_set_code.append(
                f'self.{v} = AclArray(np.array({v}, dtype = np.float32))')
        elif dtype == 'List[int]':
            attr_set_code.append(
                f'self.{v} = AclArray(np.array({v}, dtype = np.int64))')
    attr_set_str = '\n        '.join(attr_set_code)
    op_call_args = input_names + attr_call_args
    final_args = []
    ret_indexs = []
    index_offset = 0
    for i, outarg in enumerate(output_names):
        try:
            index = input_names.index(outarg)
            index_offset -= 1
        except:
            index = len(op_call_args) + i + index_offset
            final_args.append(outarg)
        ret_indexs.append(index)
    op_call_args += final_args
    args_count = len(op_call_args)
    op_call_args_str = ', '.join(op_call_args) + f',  outCout={args_count}'
    to_cpu_code = []
    if len(output_names) > 0:
        if args_count == 1:
            to_cpu_code = ['ret.to_cpu()']
        else:
            for index in ret_indexs:
                to_cpu_code.append(f'ret[{index}].to_cpu()')
    to_cpu_code_str = '\n        '.join(to_cpu_code)

    code = f'''
import ctypes
import numpy as np
from typing import List
from l0n0lacl import OpRunner, AclArray
class AscendCOp:
    def __init__(self, {attr_str}):
        {attr_set_str}
        self.op = OpRunner('{op_name}')

    def __call__(self, {run_arg_str}):
        ret = self.op({op_call_args_str})
        {to_cpu_code_str}
'''
    return code


def gen_call_arg_python_code(
        dtype_list: List[str],
        value_list: List[str],
        attr_dtype_list: List[str],
        attr_value_list: List[str]):
    args_set_code: List[str] = []
    attr_set_code: List[str] = []
    for i, dtype in enumerate(attr_dtype_list):
        v = attr_value_list[i]
        attr_set_code.append(f'self.args["{v}"]')
        args_set_code.append(f'''
    def get_{v}(self):
        return self.args['{v}']
    ''')
        args_set_code.append(f'''
    def set_{v}(self, value:{dtype}):
        self.args['{v}'] = value
    ''')
    cache = {}
    call_args = []
    for i, dtype in enumerate(dtype_list):
        v = value_list[i]
        if cache.get(v):
            continue
        cache[v] = True
        if v == 'workspace' or v == 'tiling':
            continue
        if dtype == 'GM_ADDR':
            dtype = 'np.ndarray'
        call_args.append(f'self.args["{v}"]')
        args_set_code.append(f'''
    def get_{v}(self):
        return self.args['{v}']
    ''')
        args_set_code.append(f'''
    def set_{v}(self, value:{dtype}):
        self.args['{v}'] = value
    ''')
    args_set_code = ''.join(args_set_code)
    attr_set_code_str = ', '.join(attr_set_code)
    call_args_str = ', '.join(call_args)
    
    code = f'''
import os    
import numpy as np
from typing import List
from l0n0lacltester.utils import save_ascendc_op_args, load_ascendc_op_args
current_path = os.path.split(__file__)[0]
class AscendCOpArgs:
    def __init__(self, save_file_name:str):
        self.save_file_name = f'{{current_path}}/{{save_file_name}}'
        self.args = {{}}

    def run_op(self, op_type):
        op = op_type({attr_set_code_str})
        return op({call_args_str})

    def save(self):
        save_ascendc_op_args(self.save_file_name, self.args)

    def try_load(self):
        if not os.path.exists(self.save_file_name):
            return False
        self.args = load_ascendc_op_args(self.save_file_name) 
        return True       

    def remove_record(self):
        if not os.path.exists(self.save_file_name):
            return
        os.remove(self.save_file_name)
    
    def set_arg(self, name:str, value):
        self.args[name] = value

    def get_arg(self, name:str):
        return self.args.get(name)
    
    def get_golden(self):
        return self.get_arg('golden')
        
    def set_golden(self, value):
        self.set_arg('golden', value)
    
    {args_set_code}
'''
    return code


def add_include_dirs_to_cmake_files(op_path: str, test_path: str, include_dirs: List[str]):
    with open(f'{test_path}/CMakeLists.txt') as fp:
        cmake_lists_txt_data = fp.read()
    # 移除旧的
    match = re.search(
        '# generate_includes_start[\s\S]*?# generate_includes_end', cmake_lists_txt_data)
    if match:
        cmake_lists_txt_data = cmake_lists_txt_data.replace(match.group(), '')
    include_host_str = '\n'.join(include_dirs + [
        f'{op_path}/op_host',
    ])
    include_kernel_str = '\n\t'.join(include_dirs + [
        f'{op_path}/op_kernel',
    ])
    include_codes = f'''
# generate_includes_start
include_directories(
{include_host_str})
if("${{RUN_MODE}}" STREQUAL "sim")
    ascendc_include_directories(ascendc_kernels_${{RUN_MODE}} PRIVATE \n\t{include_kernel_str})
endif()
# generate_includes_end
'''
    with open(f'{test_path}/CMakeLists.txt', 'w') as fp:
        fp.write(cmake_lists_txt_data.strip())
        fp.write(include_codes)


def generate_all_codes(op_path, test_path, include_dirs: List[str] = None, CPU_KERNEL_MODE=None):
    create_tiling(op_path, test_path, include_dirs)
    kernel_file = get_kernel_file(op_path)
    fn_name = get_kernel_function_name(op_path)
    with open(kernel_file, 'r') as file:
        content = file.read()
    function_signature = extract_function(content, fn_name)
    dtype_list, value_list = get_dtype_value_list(function_signature)
    input_names, output_names = get_op_io_name_list(op_path)
    attr_dtype_list, attr_value_list = get_attr_dtype_value(op_path)
    create_cpu(test_path, output_names, dtype_list, value_list,
               fn_name, function_signature, content, CPU_KERNEL_MODE)
    create_sim(test_path, output_names, dtype_list, value_list,
               fn_name, function_signature, content)

    python_args_code = gen_call_arg_python_code(
        dtype_list, value_list, attr_dtype_list, attr_value_list)
    with open(f'{test_path}/op_args.py', 'w') as fp:
        fp.write(python_args_code.strip())
    gpu_code = gen_npu_python_code(op_path, input_names, output_names, dtype_list,
                                   value_list, attr_dtype_list, attr_value_list)
    with open(f'{test_path}/op_npu.py', 'w') as fp:
        fp.write(gpu_code.strip())
    add_include_dirs_to_cmake_files(op_path, test_path, include_dirs)
    py_code = gen_python_code(
        dtype_list, value_list,
        output_names, attr_dtype_list, attr_value_list)
    with open(f'{test_path}/op_cpu.py', 'w') as fp:
        fp.write(py_code)


def generate_code_gen_script(op_path, test_path):
    code = f'''import os
from l0n0lacltester.gen_cpu_call_code import generate_all_codes
current_path = os.path.split(__file__)[0]
# 比如['/mnt/code/a','/mnt/code/b']
include_dirs=[
]
# enum class KernelMode {{
#     MIX_MODE = 0, # 融合模式，启用向量运算单元(aiv)与矩阵运算单元(aic)。一个block一个aic, n个aiv(n >= 1)。
#     AIC_MODE, # 仅使用矩阵运算单元(aic)。一个block仅包含一个aic。
#     AIV_MODE, # 仅使用向量运算单元(aiv)。一个block仅包含一个aiv。
#     MIX_AIC_1_1, # 矩阵运算单元(aic)与向量运算单元(aiv) 1:1合并为一个block。 一个block包含一个aiv一个aic。
# }};
CPU_KERNEL_MODE='KernelMode::AIV_MODE'
generate_all_codes('{op_path}', '.', include_dirs, CPU_KERNEL_MODE)
    '''
    with open(f'{test_path}/gen_code.py', 'w') as fp:
        fp.write(code)


def create_workspace_command():
    args = parse_args()
    op_path = args.op_path
    test_path = args.test_path
    if not os.path.exists(test_path):
        os.mkdir(test_path)
    copy_files_from_directory(
        f'{current_path}/workspace_files',
        f'{test_path}/')
    os.rename(f'{test_path}/gitignore', f'{test_path}/.gitignore')
    generate_code_gen_script(op_path, test_path)



if __name__ == '__main__':
    create_workspace_command()
