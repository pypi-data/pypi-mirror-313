#!/bin/bash
CURRENT_DIR=$(
    cd $(dirname ${BASH_SOURCE:-$0})
    pwd
)
TEST_CASE_DIR=$CURRENT_DIR
BUILD_TYPE=Debug
RUN_MODE=cpu
SOC_VERSION=Ascend910B1
REBUILD=0
while getopts "v:r:nh" opt; do
  case ${opt} in
    v )
      SOC_VERSION=${OPTARG}
      ;;
    r )
      RUN_MODE=${OPTARG}
      ;;
    n )
      REBUILD=1
      ;;
    h )
      echo "run.sh [option]"
      echo "-v 芯片型号(默认Ascend910B1)"
      echo "-r 运行模式(cpu[默认]|sim|npu)"
      echo "-n 对于cpu|sim模式不重新编译代码"
      echo "-h 显示此帮助"
      exit 0
      ;;
    \? )
      echo "不支持: -$OPTARG" 1>&2
      exit 1
      ;;
    : )
      echo "选项: -$OPTARG 需要有一个参数" 1>&2
      exit 1
      ;;
  esac
done

echo 测试用例目录:$TEST_CASE_DIR
cd $TEST_CASE_DIR
if [ -n "$ASCEND_HOME_PATH" ]; then
    if [ -d "$HOME/Ascend/ascend-toolkit/latest" ]; then
        export ASCEND_HOME_PATH="$HOME/Ascend/ascend-toolkit/latest"
    elif [ -d "$HOME/work/Ascend/ascend-toolkit/latest" ]; then
        export ASCEND_HOME_PATH="$HOME/work/Ascend/ascend-toolkit/latest"
    else
        export ASCEND_HOME_PATH=/usr/local/Ascend/ascend-toolkit/latest
    fi
fi
export ASCEND_TOOLKIT_HOME=${ASCEND_HOME_PATH}

if [ "${RUN_MODE}" = "sim" ]; then
    export LD_LIBRARY_PATH=${ASCEND_HOME_PATH}/runtime/lib64/stub:$LD_LIBRARY_PATH
    source ${ASCEND_HOME_PATH}/bin/setenv.bash
    export LD_LIBRARY_PATH=${ASCEND_HOME_PATH}/tools/simulator/${SOC_VERSION}/lib:$LD_LIBRARY_PATH
    if [ ! $CAMODEL_LOG_PATH ]; then
        export CAMODEL_LOG_PATH=$TEST_CASE_DIR/sim_log
    fi
    if [ -d "$CAMODEL_LOG_PATH" ]; then
        rm -rf $CAMODEL_LOG_PATH
    fi
    mkdir -p $CAMODEL_LOG_PATH
elif [ "${RUN_MODE}" = "cpu" ]; then
    source ${ASCEND_HOME_PATH}/bin/setenv.bash
    export LD_LIBRARY_PATH=${ASCEND_HOME_PATH}/tools/tikicpulib/lib:${ASCEND_HOME_PATH}/tools/tikicpulib/lib/${SOC_VERSION}:${_ASCEND_INSTALL_PATH}/tools/simulator/${SOC_VERSION}/lib:$LD_LIBRARY_PATH
fi
check_md5() {
    local -a paths_src=("$@") # 将所有传入的参数视为src目录
    local path_desc="$1"
    
    if [ "$#" -lt 2 ]; then
        echo "至少需要两个参数：一个目标路径和一个或多个源路径。"
        return 1
    fi

    # 移除第一个参数，它被用作描述符的路径
    paths_src=("${paths_src[@]:1}")

    local combined_md5_new=""
    
    for path_src in "${paths_src[@]}"; do
        if [ -d "$path_src" ]; then
            local md5_single=$(find "$path_src" -type f -print0 | xargs -0 md5sum | sort | md5sum | cut -d' ' -f1)
            combined_md5_new+="$md5_single"
        else
            echo "路径 '$path_src' 不是一个有效的目录。"
            return 1
        fi
    done

    # 计算所有源目录的合并后的MD5值
    md5_new=$(echo "$combined_md5_new" | md5sum | cut -d' ' -f1)

    # 检查desc目录下的md5.log是否存在并读取旧的md5值
    if [ -e "${path_desc}/md5.log" ]; then
        md5_old=$(cat "${path_desc}/md5.log")
        
        # 比较新的md5与旧的md5是否相同
        if [ "$md5_new" = "$md5_old" ]; then
            echo "MD5未改变"
            return 1
        else
            echo "MD5已改变，更新文件"
            echo "$md5_new" > "${path_desc}/md5.log"
            return 0
        fi
    else
        # 如果md5.log不存在，则直接写入新的md5值
        echo "$md5_new" > "${path_desc}/md5.log"
        echo "创建了新文件并写入MD5值"
        return 0
    fi
}

python3 $CURRENT_DIR/gen_code.py

if [ "${RUN_MODE}" = "cpu" ] || [ "${RUN_MODE}" = "sim" ]; then
    if [ $REBUILD == 0 ]; then
        rm -rf build out
        mkdir -p build
        cmake -B build -DRUN_MODE=${RUN_MODE} -DSOC_VERSION=${SOC_VERSION}
        cmake --build build -j
        cmake --install build
    fi
fi

(
    export LD_LIBRARY_PATH=$(pwd)/out/lib:$(pwd)/out/lib64:${ASCEND_HOME_PATHs}/lib64:$LD_LIBRARY_PATH
    if [[ "$WITH_MSPROF" -eq 1 ]]; then
        rm -rf ./profiles
        if [ "${RUN_MODE}" = "npu" ]; then
            msprof --application="python3 run.py ${RUN_MODE}" --output=./profiles
        elif [ "${RUN_MODE}" = "sim" ]; then
            msprof op simulator python3 run.py ${RUN_MODE} --output=./profiles
        elif [ "${RUN_MODE}" = "cpu" ]; then
            python3 run.py ${RUN_MODE}
        fi
    else
        python3 run.py ${RUN_MODE}
    fi
)



