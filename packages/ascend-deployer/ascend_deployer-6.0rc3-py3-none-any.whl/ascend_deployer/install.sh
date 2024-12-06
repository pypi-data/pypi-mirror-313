#!/bin/bash
readonly BASE_DIR=$(
    cd "$(dirname $0)" >/dev/null 2>&1
    pwd -P
)

main() {
    if [[ -f ~/.local/ascend_deployer_rc ]]; then
      source ~/.local/ascend_deployer_rc
    fi
    python3 -V > /dev/null 2>&1
    if [[ $? != 0 ]]; then
      python ${BASE_DIR}/ascend_deployer.py $*
    else
      python3 ${BASE_DIR}/ascend_deployer.py $*
    fi
}

main $*
main_status=$?
exit ${main_status}
