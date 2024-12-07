#pragma once
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <memory>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

// 总长度 + name长度 + name + value
// uint16_t + uint16_t + name + value
struct TilingDataHelper {
  char data[1024 * 1024] = {'\0'};
  uint32_t max_index = 0;
  std::unordered_map<std::string, uint32_t> index_map;
  std::unordered_map<std::string, std::string> data_cache;
  int cache_value(std::string name, size_t data_len) {
    index_map[name] = max_index;
    uint16_t *data_ptr = reinterpret_cast<uint16_t *>(data + max_index);
    // 设置总长度和name长度
    data_ptr[0] = name.size() + data_len;
    data_ptr[1] = name.size();
    // 拷贝名字
    char *name_ptr = reinterpret_cast<char *>(data_ptr + 2);
    for (size_t i = 0; i < name.size(); ++i) {
      name_ptr[i] = name.data()[i];
    }
    // 增加max_index
    max_index += name.size() + data_len + sizeof(uint16_t) * 2;
    data_cache[name] = "0";
    return 0;
  }
  template <typename T> T *get_value_ptr(std::string name) {
    auto index = index_map[name];
    auto data_ptr = data + index + sizeof(uint16_t) * 2 + name.size();
    return reinterpret_cast<T *>(data_ptr);
  }

  template <typename T> void set_value(std::string name, T value) {
    auto data_value_ptr = get_value_ptr<T>(name);
    *data_value_ptr = value;
    std::stringstream ss;
    ss << value;
    data_cache[name] = ss.str();
  }

  template <typename T>
  void set_array(std::string name, T *value, size_t value_len) {
    auto data_value_ptr = get_value_ptr<T>(name);
    std::stringstream ss;
    ss << "{";
    for (size_t i = 0; i < value_len; ++i) {
      data_value_ptr[i] = value[i];
      ss << value[i];
      if (i != value_len - 1) {
        ss << ",";
      }
    }
    ss << "}";
    data_cache[name] = ss.str();
  }
  std::string str() {
    std::stringstream ss;
    for (const auto &pair : data_cache) {
      ss << "tiling_data." << pair.first << " = " << pair.second << ";"
         << std::endl;
    }
    return ss.str();
  }

  void SaveToBuffer(char *dst, size_t capicity) {
    auto blockDim = ((int32_t *)dst)[0];
    auto alignSize = uint32_t(std::ceil(float(max_index) / 64) * 64);
    for (auto i = 0; i < blockDim; ++i) {
      ((int64_t *)(dst + i * 64))[0] = alignSize;
    }
    auto dst2 = dst + 64 * blockDim;
    for (auto i = 0; i < blockDim; ++i) {
      for (decltype(max_index) j = 0; j < max_index; ++j) {
        dst2[i * alignSize + j] = data[j];
      }
    }
    std::cout << "\033[32m" << str() << "\033[0m" << std::endl;
  }
};
#undef BEGIN_TILING_DATA_DEF
#define BEGIN_TILING_DATA_DEF(class_name)                                      \
  class class_name {                                                           \
    TilingDataHelper helper;                                                   \
                                                                               \
  public:                                                                      \
    class_name() {}
#undef TILING_DATA_FIELD_DEF
#define TILING_DATA_FIELD_DEF(data_type, field_name)                           \
public:                                                                        \
  void set_##field_name(data_type field_name) {                                \
    field_name##_ = field_name;                                                \
    helper.set_value(#field_name, field_name);                                 \
  }                                                                            \
  data_type get_##field_name() { return field_name##_; }                       \
                                                                               \
private:                                                                       \
  data_type field_name##_ = 0;                                                 \
  int field_name##_cache = helper.cache_value(#field_name, sizeof(data_type));

#undef TILING_DATA_FIELD_DEF_ARR
#define TILING_DATA_FIELD_DEF_ARR(arr_type, arr_size, field_name)              \
public:                                                                        \
  void set_##field_name(arr_type *field_name) {                                \
    for (auto i = 0; i < arr_size; ++i) {                                      \
      field_name##_[i] = field_name[i];                                        \
    }                                                                          \
    helper.set_array(#field_name, field_name, arr_size);                       \
  }                                                                            \
  arr_type *get_##field_name() { return field_name##_; }                       \
  std::size_t get_##field_name_size() { return field_name##_size_; }           \
                                                                               \
private:                                                                       \
  arr_type field_name##_[arr_size] = {0};                                      \
  std::size_t field_name##_size_ = arr_size;                                   \
  int field_name##_cache =                                                     \
      helper.cache_value(#field_name, sizeof(arr_type) * arr_size);

#undef END_TILING_DATA_DEF
#define END_TILING_DATA_DEF                                                    \
public:                                                                        \
  void SaveToBuffer(char *data, size_t capicity) {                             \
    helper.SaveToBuffer(data, capicity);                                       \
  }                                                                            \
  size_t GetDataSize() { return helper.max_index; }                            \
  }                                                                            \
  ;
