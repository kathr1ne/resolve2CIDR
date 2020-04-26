#!/bin/bash
#
#

PWD_PATH=$(cd $(dirname $BASH_SOURCE[0])&&pwd)
SET_LIST_PATH="${PWD_PATH}/result/setlist"
DST_PATH=/data/nasconfig/ipset
DST_PATH2=/data/mobile_nasconfig/ipset
SETLIST=(cn vn kr tw sg jp ru ca eu us au)
DATE=$(date +"%F %T")
log=${PWD_PATH}/log/crontab_resolve.log

resolve_txtx() {
    # https://www.ipip.net/support/db_update.html
    cp /root/ipnet/mydata4vipday2.txtx $PWD_PATH
    source ${PWD_PATH}/venv/bin/activate
    python ${PWD_PATH}/HandleTxtx.py
    if [[ $? -ne 0 ]];then
        echo "[$DATE] exec HandleTxtx.py failed, Please check" > $log
    else
        echo "[$DATE] exec HandleTxtx.py success" > $log
    fi
}

del_space() {
    sed -i '/^$/d' ${SET_LIST_PATH}/${1}.set
}

main() {
    resolve_txtx
    for list in ${SETLIST[*]};do
        del_space ${list}
        scp -q ${SET_LIST_PATH}/${list}.set 47.97.166.223:${DST_PATH}
        if [[ $? -ne 0 ]];then
            echo "[$DATE] scp to ${DST_PATH} failed, Please check" >> $log
        else
            echo "[$DATE] scp to ${DST_PATH} success" >> $log
        fi
        scp -q ${SET_LIST_PATH}/${list}.set 47.97.166.223:${DST_PATH2}
        if [[ $? -ne 0 ]];then
            echo "[$DATE] scp to ${DST_PATH2} failed, Please check" >> $log
        else
            echo "[$DATE] scp to ${DST_PATH2} success" >> $log
        fi
    done
}

main

