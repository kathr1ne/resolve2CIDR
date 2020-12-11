#!/bin/bash
#
#

PWD_PATH=$(cd $(dirname $BASH_SOURCE[0])&&pwd)
SET_LIST_PATH="${PWD_PATH}/result/setlist"
DST_PATH=/data/nasconfig/ipset
DST_PATH2=/data/mobile_nasconfig/ipset
DST_PATH3=/data/socks5d_config/ipset
SETLIST=(cn vn kr tw sg jp ru ca eu us au th hk)
DATE=$(date +"%F %T")
log=${PWD_PATH}/log/crontab_resolve.log

resolve_txtx() {
    # https://www.ipip.net/support/db_update.html
    # cp /root/ipnet/mydata4vipday2.txtx $PWD_PATH
    cp /root/ipnet/ipv4_china2_cn.txt $PWD_PATH
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

scp_file() {
    REMOTE_PATH=$1
    for list in ${SETLIST[*]};do
        del_space ${list}
        if [[ -s ${SET_LIST_PATH}/${list}.set ]];then
            cp -a ${SET_LIST_PATH}/${list}.set /data/back_ipset/
            scp -q ${SET_LIST_PATH}/${list}.set 47.97.166.223:${REMOTE_PATH}
            if [[ $? -ne 0 ]];then
                echo "[$DATE] scp $list to ${REMOTE_PATH} failed, Please check" >> $log
            else
                echo "[$DATE] scp $list to ${REMOTE_PATH} success" >> $log
            fi
        fi
    done
}

main() {
    resolve_txtx
    scp_file $DST_PATH
    scp_file $DST_PATH2
    scp_file $DST_PATH3
}

main

