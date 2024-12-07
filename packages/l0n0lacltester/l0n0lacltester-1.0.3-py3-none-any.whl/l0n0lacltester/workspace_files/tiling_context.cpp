#include "include/tiling_context.h"
#include <cstdint>

extern "C" {
void *createTilingContext() { return new gert::TilingContext(); }
void destroyTilingContext(gert::TilingContext *ptr) { delete ptr; }
void tilingContextPushInputShape(gert::TilingContext *ptr, int64_t *data,
                                 size_t len) {
  ptr->pushInputShape(data, len);
}
void tilingContextPushOutputShape(gert::TilingContext *ptr, int64_t *data,
                                  size_t len) {
  ptr->pushOutputShape(data, len);
}
void tilingContextPushPlatformInfo(gert::TilingContext *ptr, uint32_t value) {
  ptr->pushPlatformInfo(value);
}
void tilingContextSetRawTilingData(gert::TilingContext *ptr, void *data,
                                   uint64_t size) {
  ptr->setRawTilingData(data, size);
}
uint32_t tilingContextGetBlockDim(gert::TilingContext *ptr) {
  return ptr->blockDim;
}

uint64_t tilingContextGetWorkspaceSize(gert::TilingContext *ptr) {
  if (ptr->GetWorkspaceNum() == 0) {
    return 0;
  }
  return *(ptr->GetWorkspaceSizes(1));
}

void tilingContextSetAttrBool(gert::TilingContext *ptr, uint64_t index,
                              bool value) {
  ptr->setAttrBool(index, value);
}

void tilingContextSetAttrFloat(gert::TilingContext *ptr, uint64_t index,
                               float value) {
  ptr->setAttrFloat(index, value);
}

void tilingContextSetAttrInt(gert::TilingContext *ptr, uint64_t index,
                             int64_t value) {
  ptr->setAttrInt(index, value);
}

void tilingContextSetAttrString(gert::TilingContext *ptr, uint64_t index,
                                char *value, size_t len) {
  ptr->setAttrString(index, value, len);
}

void tilingContextSetAttrListBool(gert::TilingContext *ptr, uint64_t index,
                                  bool *value, size_t len) {
  ptr->setAttrListBool(index, value, len);
}

void tilingContextSetAttrListFloat(gert::TilingContext *ptr, uint64_t index,
                                   float *value, size_t len) {
  ptr->setAttrListFloat(index, value, len);
}

void tilingContextSetAttrListInt(gert::TilingContext *ptr, uint64_t index,
                                 int64_t *value, size_t len) {
  ptr->setAttrListInt(index, value, len);
}

void tilingContextPushInputDesc(gert::TilingContext *ptr, uint32_t dtype) {
  ptr->pushInputDesc(dtype);
}

void tilingContextPushOutputDesc(gert::TilingContext *ptr, uint32_t dtype) {
  ptr->pushOutputDesc(dtype);
}
}