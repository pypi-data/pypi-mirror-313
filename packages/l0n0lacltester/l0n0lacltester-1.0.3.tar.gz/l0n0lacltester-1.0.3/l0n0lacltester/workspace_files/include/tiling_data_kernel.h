#pragma once
#include "kernel_operator.h"
#include <cstdint>
namespace AscendC {
// 总长度 + name长度 + name + 指针
// uint16_t + uint16_t + name + 指针
struct TilingDataHelper {
  GM_ADDR gData;
  GlobalTensor<uint8_t> gT;
  int64_t size;
  __aicore__ inline TilingDataHelper(){};
  __aicore__ inline void init(GM_ADDR data) {
    auto blockIdx = GetBlockIdx();
    size = ((__gm__ int64_t *)(data + blockIdx * 64))[0];
    gT.SetGlobalBuffer(data + GetBlockNum() * 64 + blockIdx * size, size);
  }
  __aicore__ inline bool str_eq(const __gm__ char *a, GlobalTensor<uint8_t> b,
                                int len) {
    GlobalTensor<uint8_t> aT;
    aT.SetGlobalBuffer((GM_ADDR)a);
    for (int i = 0; i < len; ++i) {
      if (aT(i) != b(i)) {
        return false;
      }
    }
    return true;
  }

  __aicore__ inline int str_length(const __gm__ char *a) {
    int len = 0;
    while (a[len] != '\0') {
      len++;
    }
    return len;
  }
  __aicore__ inline int load_value(const __gm__ char *name, uint8_t *dst,
                                   int data_len) {
    int name_len = str_length(name);
    int index = 0;
    while (index < size) {
      uint16_t node_len = 0;
      uint16_t node_name_len = 0;
      ((uint8_t *)&node_len)[0] = gT(index + 0);
      ((uint8_t *)&node_len)[1] = gT(index + 1);
      ((uint8_t *)&node_name_len)[0] = gT(index + 2);
      ((uint8_t *)&node_name_len)[1] = gT(index + 3);
      if (name_len == node_name_len) {
        auto name_index = index + sizeof(uint16_t) * 2;
        if (str_eq(name, gT[name_index], node_name_len)) {
          for (int i = 0; i < data_len; ++i) {
            dst[i] = gT(name_index + name_len + i);
          }
          return 1;
        }
      }
      index += sizeof(uint16_t) * 2 + node_len;
    }
    return 0;
  }
};

#define BEGIN_KERNEL_TILING_DATA_DEF(class_name) struct class_name {

#define TILING_KERNEL_DATA_FIELD_DEF(data_type, field_name)                    \
  data_type field_name = 0;

#define TILING_KERNEL_DATA_FIELD_DEF_ARR(arr_type, arr_size, field_name)       \
  arr_type field_name[arr_size] = {0};

#define END_KERNEL_TILING_DATA_DEF                                             \
  }                                                                            \
  ;

#define TILING_LOAD_FIELD(helper, cls, data_type, field_name)                  \
  helper.load_value(#field_name, (uint8_t *)&cls.field_name, sizeof(data_type));

#define TILING_LOAD_ARR(helper, cls, arr_type, arr_size, field_name)           \
  helper.load_value(#field_name, (uint8_t *)&cls.field_name,                   \
                    sizeof(arr_type) * arr_size);
} // namespace AscendC
