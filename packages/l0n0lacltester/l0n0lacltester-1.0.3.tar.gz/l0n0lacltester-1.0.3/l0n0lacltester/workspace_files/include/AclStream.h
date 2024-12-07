#pragma once
#include "acl/acl.h"
#include "utils.h"

class AclStream {
public:
  aclrtStream stream = nullptr;
  AclStream() { aclrtCreateStream(&stream); };
  ~AclStream() {
    sync();
    aclrtDestroyStream(stream);
  };
  void sync() {
    aclrtStreamStatus status;
    auto ret = aclrtStreamQuery(stream, &status);
    CHECK_ACL_RET(ret, "aclStream::sync::aclrtStreamQuery")
    if (status == aclrtStreamStatus::ACL_STREAM_STATUS_NOT_READY) {
      ret = aclrtSynchronizeStream(stream);
      CHECK_ACL_RET(ret, "aclStream::sync::aclrtSynchronizeStream")
    }
  }
  void *getPtr() { return stream; }
};