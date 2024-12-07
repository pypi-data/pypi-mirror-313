#pragma once
#include "acl/acl.h"
#include "utils.h"
#include <cstdint>
#include <sstream>
#include <string>
class AclMemory {
public:
  void *devicePtr = nullptr;
  size_t mem_size = 0;
  size_t data_size = 0;
  void *hostPtr = nullptr;

public:
  AclMemory() {}
  AclMemory(size_t size) { mallocDevMemory(size); };
  AclMemory(size_t size, void *hostPtr) {
    mallocDevMemory(size);
    this->hostPtr = hostPtr;
    copyFromHost(hostPtr, size);
  };
  ~AclMemory() {
    if (devicePtr) {
      aclrtFree(devicePtr);
      devicePtr = nullptr;
    }
  };
  void mallocDevMemory(size_t size) {
    if (size == 0) {
      return;
    }
    data_size = size;
    mem_size = ALIGN_TO(size, 32);
    auto ret = aclrtMalloc(&devicePtr, size,
                           aclrtMemMallocPolicy::ACL_MEM_MALLOC_HUGE_FIRST);
    CHECK_ACL_RET(ret, "AclMemory::mallocDevMemory");
  }

  void copyFromHost(void *hostPtr, size_t copySize) {
    if (mem_size == 0) {
      return;
    }
    auto ret = aclrtMemcpy(devicePtr, copySize, hostPtr, copySize,
                           aclrtMemcpyKind::ACL_MEMCPY_HOST_TO_DEVICE);
    CHECK_ACL_RET(ret, "AclMemory::copyFromHost");
  }
  void copyToHost(void *hostPtr, size_t copySize) {
    if (mem_size == 0) {
      return;
    }
    auto ret = aclrtMemcpy(hostPtr, copySize, devicePtr, copySize,
                           aclrtMemcpyKind::ACL_MEMCPY_DEVICE_TO_HOST);
    CHECK_ACL_RET(ret, "AclMemory::copyToHost");
  }
  void toHost() { copyToHost(hostPtr, data_size); }
  uint8_t *devPtr() { return (uint8_t *)devicePtr; }
};
