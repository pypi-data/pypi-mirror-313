#pragma once
#include "tiling/platform/platform_ascendc.h"
#include "tiling_data_desc.h"
#include "tiling_shape.h"
#include <type_traits>
#include <vector>
namespace gert {

struct RawTilingData {
  char *data_ptr = nullptr;
  size_t capicity = 0;
  size_t data_size = 0;
  char *GetData() { return data_ptr; }
  size_t GetCapacity() { return capicity; }
  void SetDataSize(size_t v) { data_size = v; }
};

template <typename T> struct TlingAttrListValue {
  T *data = nullptr;
  size_t len = 0;
  ~TlingAttrListValue() {
    if (data) {
      delete[] data;
      data = nullptr;
    }
  }
  void copyList(T *dst, T *from, size_t len) {
    for (size_t i = 0; i < len; ++i) {
      dst[i] = from[i];
    }
  }

  void set(T *value, size_t value_len) {
    if (data) {
      delete[] data;
      data = nullptr;
    }

    if (typeid(T) == typeid(char)) {
      data = new T[value_len + 1];
      std::strcpy((char *)data, (char *)value);
    } else {
      data = new T[value_len];
      copyList(data, value, value_len);
    }
    len = value_len;
  }

  T *GetData() { return data; }
  size_t getSize() { return len; }
};

enum class TilingAttrDtype {
  NONE = 0,
  BOOL,
  INT,
  FLOAT,
  STRING,
  LIST_BOOL,
  LIST_INT,
  LIST_FLOAT,
};

struct TilingAttrs {
  std::vector<void *> attrs_;
  std::vector<TilingAttrDtype> attrs_types_;
  TilingAttrs() {
    for (size_t i = 0; i < 1024; ++i) {
      attrs_.push_back(0);
      attrs_types_.push_back(TilingAttrDtype::NONE);
    }
  }
  ~TilingAttrs() {
    for (size_t i = 0; i < attrs_.size(); ++i) {
      TilingAttrDtype dtype = attrs_types_[i];
      auto p = attrs_[i];
      if (!p) {
        continue;
      }
      switch (dtype) {
      case TilingAttrDtype::BOOL:
        delete (bool *)p;
        break;
      case TilingAttrDtype::INT:
        delete (int64_t *)p;
        break;
      case TilingAttrDtype::FLOAT:
        delete (float *)p;
        break;
      case TilingAttrDtype::STRING:
        delete (TlingAttrListValue<char> *)p;
        break;
      case TilingAttrDtype::LIST_BOOL:
        delete (TlingAttrListValue<bool> *)p;
        break;
      case TilingAttrDtype::LIST_INT:
        delete (TlingAttrListValue<int64_t> *)p;
        break;
      case TilingAttrDtype::LIST_FLOAT:
        delete (TlingAttrListValue<float> *)p;
        break;
      case TilingAttrDtype::NONE:
        break;
      }
    }
  }
  void setAttrBool(uint64_t index, bool value) {
    auto p = new bool;
    *p = value;
    attrs_[index] = p;
    attrs_types_[index] = TilingAttrDtype::BOOL;
  }
  void setAttrFloat(uint64_t index, float value) {
    auto p = new float;
    *p = value;
    attrs_[index] = p;
    attrs_types_[index] = TilingAttrDtype::FLOAT;
  }
  void setAttrInt(uint64_t index, int64_t value) {
    auto p = new int64_t;
    *p = value;
    attrs_[index] = p;
    attrs_types_[index] = TilingAttrDtype::INT;
  }
  void setAttrString(uint64_t index, char *value, size_t len) {
    auto p = new TlingAttrListValue<char>;
    p->set(value, len);
    attrs_[index] = p;
    attrs_types_[index] = TilingAttrDtype::STRING;
  }
  void setAttrListBool(uint64_t index, bool *value, size_t len) {
    auto p = new TlingAttrListValue<bool>;
    p->set(value, len);
    attrs_[index] = p;
    attrs_types_[index] = TilingAttrDtype::LIST_BOOL;
  }
  void setAttrListFloat(uint64_t index, float *value, size_t len) {
    auto p = new TlingAttrListValue<float>;
    p->set(value, len);
    attrs_[index] = p;
    attrs_types_[index] = TilingAttrDtype::LIST_FLOAT;
  }
  void setAttrListInt(uint64_t index, int64_t *value, size_t len) {
    auto p = new TlingAttrListValue<int64_t>;
    p->set(value, len);
    attrs_[index] = p;
    attrs_types_[index] = TilingAttrDtype::LIST_INT;
  }
  const bool *GetBool(uint64_t index) {
    return reinterpret_cast<bool *>(attrs_[index]);
  }
  const uint64_t *GetInt(uint64_t index) {
    return reinterpret_cast<uint64_t *>(attrs_[index]);
  }
  const float *GetFloat(uint64_t index) {
    return reinterpret_cast<float *>(attrs_[index]);
  }
  const char *GetStr(uint64_t index) {
    return reinterpret_cast<TlingAttrListValue<char> *>(attrs_[index])->data;
  }
  const TlingAttrListValue<bool> *GetListBool(uint64_t index) {
    return reinterpret_cast<TlingAttrListValue<bool> *>(attrs_[index]);
  }
  const TlingAttrListValue<int64_t> *GetListInt(uint64_t index) {
    return reinterpret_cast<TlingAttrListValue<int64_t> *>(attrs_[index]);
  }
  const TlingAttrListValue<float> *GetListFloat(uint64_t index) {
    return reinterpret_cast<TlingAttrListValue<float> *>(attrs_[index]);
  }
};

struct TilingContext {
  std::vector<StorageShape> input_shapes_;
  std::vector<CompileTimeTensorDesc> input_desc_;
  std::vector<StorageShape> output_shapes_;
  std::vector<CompileTimeTensorDesc> output_desc_;
  std::vector<size_t> workspace_sizes_;
  std::vector<uint32_t> platform_info_;
  RawTilingData raw_tiling_data_;
  uint32_t blockDim = 0;
  TilingAttrs attrs_;

  TilingContext() {}

  StorageShape createStorageShape(int64_t *data, size_t len) {
    StorageShape shape;
    shape.MutableOriginShape().SetDimNum(len);
    shape.MutableStorageShape().SetDimNum(len);
    for (size_t i = 0; i < len; ++i) {
      shape.MutableOriginShape().SetDim(i, data[i]);
      shape.MutableStorageShape().SetDim(i, data[i]);
    }
    return shape;
  }

  void pushInputShape(int64_t *data, size_t len) {
    input_shapes_.push_back(createStorageShape(data, len));
  }

  const StorageShape *GetInputShape(const size_t index) const {
    return input_shapes_.data() + index;
  }

  void pushOutputShape(int64_t *data, size_t len) {
    output_shapes_.push_back(createStorageShape(data, len));
  }

  const StorageShape *GetOutputShape(const size_t index) const {
    return output_shapes_.data() + index;
  }

  void pushPlatformInfo(uint32_t value) { platform_info_.push_back(value); }
  /**
   * 获取workspace sizes指针
   * @param workspace_count
   * workspace的个数，传入的workspace个数不可以超过编译时指定的最大workspace个数
   * @return workspace sizes指针
   */
  size_t *GetWorkspaceSizes(const size_t workspace_count) {
    while (workspace_sizes_.size() < workspace_count) {
      workspace_sizes_.push_back(0);
    }
    return workspace_sizes_.data() + workspace_count - 1;
  }
  /**
   * 获取 workspace 个数
   * @return workspace 个数
   */
  size_t GetWorkspaceNum() const { return workspace_sizes_.size(); }

  uint32_t *GetPlatformInfo() { return platform_info_.data(); }

  void SetBlockDim(uint32_t value) {
    blockDim = value;
    ((uint32_t *)raw_tiling_data_.GetData())[0] = value;
  }
  uint32_t getBlockDim() { return blockDim; }

  RawTilingData *GetRawTilingData() { return &raw_tiling_data_; }

  void setRawTilingData(void *data_ptr, size_t capicity) {
    raw_tiling_data_.data_ptr = (char *)data_ptr;
    raw_tiling_data_.capicity = capicity;
  }
  void setAttrBool(uint64_t index, bool value) {
    attrs_.setAttrBool(index, value);
  }
  void setAttrFloat(uint64_t index, float value) {
    attrs_.setAttrFloat(index, value);
  }
  void setAttrInt(uint64_t index, int64_t value) {
    attrs_.setAttrInt(index, value);
  }
  void setAttrString(uint64_t index, char *value, size_t len) {
    attrs_.setAttrString(index, value, len);
  }
  void setAttrListBool(uint64_t index, bool *value, size_t len) {
    attrs_.setAttrListBool(index, value, len);
  }
  void setAttrListFloat(uint64_t index, float *value, size_t len) {
    attrs_.setAttrListFloat(index, value, len);
  }
  void setAttrListInt(uint64_t index, int64_t *value, size_t len) {
    attrs_.setAttrListInt(index, value, len);
  }
  TilingAttrs *GetAttrs() { return &attrs_; }

  const CompileTimeTensorDesc *GetInputDesc(const size_t index) const {
    return input_desc_.data() + index;
  }

  void pushInputDesc(uint32_t dtype) {
    CompileTimeTensorDesc desc;
    desc.SetDataType((ge::DataType)dtype);
    input_desc_.push_back(desc);
  }

  const CompileTimeTensorDesc *GetOutputDesc(const size_t index) const {
    return output_desc_.data() + index;
  }

  void pushOutputDesc(uint32_t dtype) {
    CompileTimeTensorDesc desc;
    desc.SetDataType((ge::DataType)dtype);
    output_desc_.push_back(desc);
  }
  int SetScheduleMode(const uint32_t schedule_mode) { return 0; }
};
} // namespace gert