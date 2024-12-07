#pragma once
#include "tikicpulib.h"
#include "utils.h"
class AclGmMemory {
public:
  void *devicePtr = nullptr;
  size_t mem_size = 0;
  size_t data_size = 0;
  void *hostPtr = nullptr;

public:
  AclGmMemory() {}
  AclGmMemory(size_t size) { mallocDevMemory(size); };
  AclGmMemory(size_t size, void *hostPtr) {
    mallocDevMemory(size);
    this->hostPtr = hostPtr;
    copyFromHost(hostPtr, size);
  };
  ~AclGmMemory() {
    if (devicePtr) {
      AscendC::GmFree(devicePtr);
      devicePtr = nullptr;
    }
  };
  void mallocDevMemory(size_t size) {
    if (size == 0) {
      return;
    }
    data_size = size;
    mem_size = ALIGN_TO(size, 32);
    devicePtr = AscendC::GmAlloc(mem_size);
  }
  void copyFromHost(void *hostPtr, size_t copySize) {
    if (mem_size == 0) {
      return;
    }
    memcpy(devicePtr, hostPtr, copySize);
  }
  void copyToHost(void *hostPtr, size_t copySize) {
    if (mem_size == 0) {
      return;
    }
    memcpy(hostPtr, devicePtr, copySize);
  }
  void toHost() { copyToHost(hostPtr, data_size); }
  GM_ADDR devPtr() { return (GM_ADDR)devicePtr; }
};
