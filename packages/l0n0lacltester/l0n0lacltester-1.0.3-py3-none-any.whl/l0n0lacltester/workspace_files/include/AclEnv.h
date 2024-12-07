#pragma once
#include "acl/acl.h"
#include <cstdint>
#include <iostream>
class AclEnv {
public:
  int32_t deviceId;
  AclEnv(int32_t deviceId = 0) : deviceId(deviceId) {
    aclInit(nullptr);
    aclrtSetDevice(deviceId);
  };
  ~AclEnv() {
    aclrtResetDevice(deviceId);
    aclFinalize();
  };
};