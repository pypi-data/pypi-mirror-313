#pragma once
#include <iostream>
#include <sstream>
#define CHECK_ACL_RET(ret, errorMsg)                                           \
  if (ret != ACL_SUCCESS) {                                                    \
    std::stringstream ss;                                                      \
    ss << "\033[31m";                                                          \
    ss << errorMsg;                                                            \
    ss << " ret = ";                                                           \
    ss << ret;                                                                 \
    ss << "!\033[0m";                                                          \
    std::cout << ss.str() << std::endl;                                        \
  }
#ifndef CEIL_DIV
#define CEIL_DIV(a, b) (((a) + (b)-1) / (b))
#endif
#ifndef ALIGN_TO
#define ALIGN_TO(a, b) CEIL_DIV(a, b) * (b)
#endif
