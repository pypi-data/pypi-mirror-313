cmake_minimum_required(VERSION 3.16)
project(Ascend_c)

set(RUN_MODE "npu" CACHE STRING "运行模式(cpu|sim)")
set(SOC_VERSION "Ascend910B1" CACHE STRING "芯片型号(默认Ascend910B1)")
set(ASCEND_HOME_PATH $ENV{ASCEND_HOME_PATH})
set(ASCEND_CANN_PACKAGE_PATH ${ASCEND_HOME_PATH})
message("ASCEND_HOME_PATH = ${ASCEND_HOME_PATH}")
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Debug" CACHE STRING "构建类型Release/Debug(默认Debug)" FORCE)
endif()
set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}/out" CACHE STRING "安装目录" FORCE)
if("${RUN_MODE}" STREQUAL "cpu")
    file(GLOB KERNEL_FILES ${CMAKE_CURRENT_SOURCE_DIR}/cpu/kernel.cpp)
    include("cmake/cpu_lib.cmake")
    add_library(ascendc_kernels_bbit SHARED
        ${CMAKE_CURRENT_SOURCE_DIR}/cpu/lib.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/tiling.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/tiling_context.cpp
    )
elseif("${RUN_MODE}" STREQUAL "sim")
    file(GLOB KERNEL_FILES ${CMAKE_CURRENT_SOURCE_DIR}/sim/kernel.cpp)
    include("cmake/npu_lib.cmake")
    add_library(ascendc_kernels_bbit SHARED
        ${CMAKE_CURRENT_SOURCE_DIR}/sim/lib.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/tiling.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/tiling_context.cpp
    )
else()
    message("运行模式错误 RUN_MODE: ${RUN_MODE}")
endif()

target_compile_definitions(ascendc_kernels_bbit PRIVATE
    MY_ASCENDC_SOC_VERSION="${SOC_VERSION}"
)
target_compile_options(ascendc_kernels_bbit PRIVATE
    $<BUILD_INTERFACE:$<$<STREQUAL:${RUN_MODE},cpu>:-g>>
    -O2 -std=c++17 -D_GLIBCXX_USE_CXX11_ABI=0 -Wall -Werror
)
target_link_libraries(ascendc_kernels_bbit PRIVATE
    tiling_api
    platform
    $<BUILD_INTERFACE:$<$<OR:$<STREQUAL:${RUN_MODE},npu>,$<STREQUAL:${RUN_MODE},sim>>:host_intf_pub>>
    $<BUILD_INTERFACE:$<$<STREQUAL:${RUN_MODE},cpu>:ascendcl>>
    ascendc_kernels_${RUN_MODE}
)
install(TARGETS ascendc_kernels_bbit
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
