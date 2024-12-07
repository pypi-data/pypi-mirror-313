import os
import json
import shutil
import base64
import colorama
import numpy as np


def print_red(*args):
    print(colorama.Fore.RED, end='', flush=True)
    print(*args, end='', flush=True)
    print(colorama.Style.RESET_ALL, flush=True)


def print_green(*args):
    print(colorama.Fore.GREEN, end='', flush=True)
    print(*args, end='', flush=True)
    print(colorama.Style.RESET_ALL, flush=True)


def print_yellow(*args):
    print(colorama.Fore.YELLOW, end='', flush=True)
    print(*args, end='', flush=True)
    print(colorama.Style.RESET_ALL, flush=True)


def print_blue(*args):
    print(colorama.Fore.BLUE, end='', flush=True)
    print(*args, end='', flush=True)
    print(colorama.Style.RESET_ALL, flush=True)


def print_cyan(*args):
    print(colorama.Fore.CYAN, end='', flush=True)
    print(*args, end='', flush=True)
    print(colorama.Style.RESET_ALL, flush=True)


def copy_files_from_directory(src_dir, dest_dir):
    # 确保目标目录存在
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 遍历源目录中的所有文件和子目录
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)

        # 如果是文件，则拷贝文件
        if os.path.isfile(s):
            shutil.copy2(s, d)  # 使用 copy2 可以保留文件的元数据
        # 如果是目录，则递归拷贝整个目录
        elif os.path.isdir(s):
            try:
                shutil.rmtree(d)
            except:
                pass
            shutil.copytree(s, d)


def encode_numpy_array(arr: np.ndarray) -> str:
    """Encode a numpy ndarray to a base64 string."""
    return base64.b64encode(arr.tobytes()).decode('utf-8')


def decode_numpy_array(b64_str: str, dtype: np.dtype, shape: tuple) -> np.ndarray:
    """Decode a base64 string back into a numpy ndarray."""
    data = base64.b64decode(b64_str)
    return np.frombuffer(data, dtype=dtype).reshape(shape)


def encode_data(data):
    if isinstance(data, np.ndarray):
        return {
            "__type__": "numpy.ndarray",
            "dtype": data.dtype.str,
            "shape": data.shape,
            "data": encode_numpy_array(data)
        }
    elif isinstance(data, bytes):
        return {
            "__type__": "bytes",
            "data": data.decode()
        }
    return data


def decode_data(data):
    if isinstance(data, dict) and "__type__" in data:
        dtype = data.get("dtype")
        shape = data.get("shape")
        if data["__type__"] == "numpy.ndarray":
            return decode_numpy_array(data["data"], dtype=dtype, shape=shape)
        elif data["__type__"] == "bytes":
            return data["data"].encode()
    return data


def custom_encoder(o):
    """Custom JSON encoder for numpy arrays and bytes."""
    if isinstance(o, np.ndarray):
        return encode_data(o)
    elif isinstance(o, bytes):
        return encode_data(o)
    raise TypeError(
        f"Object of type {o.__class__.__name__} is not JSON serializable")


def custom_decoder(dct):
    """Custom JSON decoder for numpy arrays and bytes."""
    if "__type__" in dct:
        return decode_data(dct)
    return dct


def save_ascendc_op_args(save_file_name: str, args: dict):
    with open(save_file_name, 'w') as f:
        json.dump(args, f, indent='\t', default=custom_encoder)


def load_ascendc_op_args(load_file_name: str) -> dict:
    with open(load_file_name, 'r') as f:
        return json.load(f, object_hook=custom_decoder)
