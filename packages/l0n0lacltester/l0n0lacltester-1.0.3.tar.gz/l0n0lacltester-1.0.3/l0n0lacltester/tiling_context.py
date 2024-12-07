import ctypes
from typing import List
import numpy as np


class AclDtype:
    ACL_DT_UNDEFINED = -1  # 未知数据类型，默认值
    ACL_FLOAT = 0
    ACL_FLOAT16 = 1
    ACL_INT8 = 2
    ACL_INT32 = 3
    ACL_UINT8 = 4
    ACL_INT16 = 6
    ACL_UINT16 = 7
    ACL_UINT32 = 8
    ACL_INT64 = 9
    ACL_UINT64 = 10
    ACL_DOUBLE = 11
    ACL_BOOL = 12
    ACL_STRING = 13
    ACL_COMPLEX64 = 16
    ACL_COMPLEX128 = 17
    ACL_BF16 = 27
    ACL_INT4 = 29
    ACL_UINT1 = 30
    ACL_COMPLEX32 = 33


class TilingContext:
    def __init__(self, lib: ctypes.CDLL):
        self.lib = lib
        self.raw_tiling_data = np.zeros(1024*1024, dtype=np.uint8)

        # 设置函数的参数和返回类型
        self.createTilingContext = self.lib.createTilingContext
        self.createTilingContext.restype = ctypes.c_void_p

        self.destroyTilingContext = self.lib.destroyTilingContext
        self.destroyTilingContext.argtypes = [ctypes.c_void_p]

        self.tilingContextPushInputShape = self.lib.tilingContextPushInputShape
        self.tilingContextPushInputShape.argtypes = [
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]

        self.tilingContextPushOutputShape = self.lib.tilingContextPushOutputShape
        self.tilingContextPushOutputShape.argtypes = [
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]

        self.tilingContextPushPlatformInfo = self.lib.tilingContextPushPlatformInfo
        self.tilingContextPushPlatformInfo.argtypes = [
            ctypes.c_void_p, ctypes.c_uint32]

        self.tilingContextSetRawTilingData = self.lib.tilingContextSetRawTilingData
        self.tilingContextSetRawTilingData.argtypes = [
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint64]

        self.tilingContextGetBlockDim = self.lib.tilingContextGetBlockDim
        self.tilingContextGetBlockDim.argtypes = [ctypes.c_void_p]
        self.tilingContextGetBlockDim.restype = ctypes.c_uint32

        self.tilingContextGetWorkspaceSize = self.lib.tilingContextGetWorkspaceSize
        self.tilingContextGetWorkspaceSize.argtypes = [ctypes.c_void_p]
        self.tilingContextGetWorkspaceSize.restype = ctypes.c_uint64

        self.tilingContextSetAttrBool = self.lib.tilingContextSetAttrBool
        self.tilingContextSetAttrBool.argtypes = [
            ctypes.c_void_p, ctypes.c_uint64, ctypes.c_bool]

        self.tilingContextSetAttrFloat = self.lib.tilingContextSetAttrFloat
        self.tilingContextSetAttrFloat.argtypes = [
            ctypes.c_void_p, ctypes.c_uint64, ctypes.c_float]

        self.tilingContextSetAttrString = self.lib.tilingContextSetAttrString
        self.tilingContextSetAttrString.argtypes = [
            ctypes.c_void_p, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_size_t]

        self.tilingContextSetAttrInt = self.lib.tilingContextSetAttrInt
        self.tilingContextSetAttrInt.argtypes = [
            ctypes.c_void_p, ctypes.c_uint64, ctypes.c_int64]

        self.tilingContextSetAttrListBool = self.lib.tilingContextSetAttrListBool
        self.tilingContextSetAttrListBool.argtypes = [
            ctypes.c_void_p, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_size_t]

        self.tilingContextSetAttrListFloat = self.lib.tilingContextSetAttrListFloat
        self.tilingContextSetAttrListFloat.argtypes = [
            ctypes.c_void_p, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_size_t]

        self.tilingContextSetAttrListInt = self.lib.tilingContextSetAttrListInt
        self.tilingContextSetAttrListInt.argtypes = [
            ctypes.c_void_p, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_size_t]

        self.tilingContextPushInputDesc = self.lib.tilingContextPushInputDesc
        self.tilingContextPushInputDesc.argtypes = [
            ctypes.c_void_p, ctypes.c_uint32]

        self.tilingContextPushOutputDesc = self.lib.tilingContextPushOutputDesc
        self.tilingContextPushOutputDesc.argtypes = [
            ctypes.c_void_p, ctypes.c_uint32]

        # 创建一个上下文实例
        self.context_ptr = self.createTilingContext()
        self.set_raw_tiling_data()

    def __del__(self):
        """销毁时自动释放资源"""
        if self.context_ptr:
            self.destroyTilingContext(self.context_ptr)

    def push_input_shape(self, data: list):
        """推入输入形状数据"""
        int64_data = np.array(data, dtype=np.int64)
        self.tilingContextPushInputShape(
            self.context_ptr, int64_data.ctypes.data, int64_data.size)

    def push_output_shape(self, data: list):
        """推入输出形状数据"""
        int64_data = np.array(data, dtype=np.int64)
        self.tilingContextPushOutputShape(
            self.context_ptr, int64_data.ctypes.data, int64_data.size)

    def push_platform_info(self, value: int):
        """推入平台信息"""
        self.tilingContextPushPlatformInfo(self.context_ptr, value)

    def set_raw_tiling_data(self):
        """设置原始分块数据"""
        self.tilingContextSetRawTilingData(
            self.context_ptr, self.raw_tiling_data.ctypes.data, self.raw_tiling_data.size)

    def get_block_dim(self):
        return self.tilingContextGetBlockDim(self.context_ptr)

    def get_workspace_size(self):
        return self.tilingContextGetWorkspaceSize(self.context_ptr)

    def set_attr_bool(self, index: int, value: bool):
        """设置布尔属性"""
        self.tilingContextSetAttrBool(self.context_ptr, index, value)

    def set_attr_float(self, index: int, value: float):
        """设置浮点属性"""
        self.tilingContextSetAttrFloat(self.context_ptr, index, value)

    def set_attr_int(self, index: int, value: int):
        """设置整数属性"""
        self.tilingContextSetAttrInt(self.context_ptr, index, value)

    def set_attr_string(self, index: int, value: str):
        """设置字符串属性"""
        c_value = value.encode()
        length = len(value)
        self.tilingContextSetAttrString(
            self.context_ptr, index, c_value, length)

    def set_attr_list_bool(self, index: int, values: List[bool]):
        """设置布尔列表属性"""
        bool_array = np.array(values, dtype=np.bool_)
        self.tilingContextSetAttrListBool(
            self.context_ptr, index, bool_array.ctypes.data, bool_array.size)

    def set_attr_list_float(self, index: int, values: List[float]):
        """设置浮点列表属性"""
        float_array = np.array(values, dtype=np.float32)
        self.tilingContextSetAttrListFloat(
            self.context_ptr, index, float_array.ctypes.data, float_array.size)

    def set_attr_list_int(self, index: int, values: List[int]):
        """设置整数列表属性"""
        int_array = np.array(values, dtype=np.int64)
        self.tilingContextSetAttrListInt(
            self.context_ptr, index, int_array.ctypes.data, int_array.size)

    def numpy_dtype_2_acl_dtype(self, numpy_dtype) -> int:
        if numpy_dtype == np.float32:
            return AclDtype.ACL_FLOAT
        if numpy_dtype == np.float16:
            return AclDtype.ACL_FLOAT16
        if numpy_dtype == np.int8:
            return AclDtype.ACL_INT8
        if numpy_dtype == np.int32:
            return AclDtype.ACL_INT32
        if numpy_dtype == np.uint8:
            return AclDtype.ACL_UINT8
        if numpy_dtype == np.int16:
            return AclDtype.ACL_INT16
        if numpy_dtype == np.uint16:
            return AclDtype.ACL_UINT16
        if numpy_dtype == np.uint32:
            return AclDtype.ACL_UINT32
        if numpy_dtype == np.int64:
            return AclDtype.ACL_INT64
        if numpy_dtype == np.uint64:
            return AclDtype.ACL_UINT64
        if numpy_dtype == np.double:
            return AclDtype.ACL_DOUBLE
        if numpy_dtype == np.bool_:
            return AclDtype.ACL_BOOL
        if numpy_dtype == np.complex64:
            return AclDtype.ACL_COMPLEX64
        if numpy_dtype == np.complex128:
            return AclDtype.ACL_COMPLEX128

    def push_input_desc(self, dtype: np.dtype):
        acl_dtype: int = self.numpy_dtype_2_acl_dtype(dtype)
        self.tilingContextPushInputDesc(self.context_ptr, acl_dtype)

    def push_output_desc(self, dtype: np.dtype):
        acl_dtype: int = self.numpy_dtype_2_acl_dtype(dtype)
        self.tilingContextPushOutputDesc(self.context_ptr, acl_dtype)
