#!/bin/bash
readonly BASE_DIR=$(cd "$(dirname $0)" > /dev/null 2>&1; pwd -P)


function main()
{
    python3 -V > /dev/null 2>&1
    if [[ $? != 0 ]]; then
        echo "python3 is not available, install it first by running 'apt install -y python3' or 'yum install -y python3' with root permission and available repo accessing"
        return 1
    else
        python3 ${BASE_DIR}/ascend_download.py $@
        return $?
    fi
}

main $*
main_status=$?
exit ${main_status}
