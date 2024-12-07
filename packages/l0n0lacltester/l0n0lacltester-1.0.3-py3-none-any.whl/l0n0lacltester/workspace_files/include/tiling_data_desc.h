#pragma once
#include "graph/types.h"
struct CompileTimeTensorDesc {
  ge::DataType data_type_;
  ge::DataType GetDataType() const { return data_type_; }
  void SetDataType(const ge::DataType data_type) { data_type_ = data_type; }
};