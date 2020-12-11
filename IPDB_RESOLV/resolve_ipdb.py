#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


import os
import ipdb
import multiprocessing
from netaddr import IPNetwork
from time import time


def resolve_ipdb(ip, index):
    s = time()
    print("Start: Thread-{} Search: CIDR-{}".format(index, ip))
    for i in ip:
        r = db.find(i, 'CN')
        # r = [str(i), r[0], r[1], r[-2], r[-1]]
        r = [str(i), r[0], r[-2], r[-1]]
        dic[index].append((' '.join(r) + '\n'))
    e = time()
    print("Finished: Thread-{} speed time {:.4f}s".format(index, e - s))

    # save_name = os.path.join(basedir, 'txtx', 'ip_data_{}.txtx'.format(str(index).zfill(3)))
    save_name = os.path.join('/data/resolve_result/txtx', 'ip_data_{}.txtx'.format(str(index).zfill(3)))
    with open(save_name, 'w') as txtx_file:
        txtx_file.writelines(dic[index])


def multi_process(start, step):
    procs = []
    end = start + step
    print("##### CIDR RANGE: {}.0.0.0/8 - {}.0.0.0/8. #####".format(start, end - 1))
    for i in range(start, end):
        dic[i] = []
        try:
            ip = IPNetwork('{}.0.0.0/8'.format(i))
        except Exception as e:
            return False
        p = multiprocessing.Process(target=resolve_ipdb, args=(ip, i))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    return multiprocessing.active_children()


if __name__ == '__main__':
    # basedir = os.path.abspath(os.path.dirname(__file__))
    s = time()
    db = ipdb.City("/home/kongs/resolve2CIDR/mydata4vipday2.ipdb")
    i = 0
    step = 16
    dic = {}
    result = multi_process(i, step)
    while True:
        i += step
        if i == 256:
            break
        result = multi_process(i, step)
    e = time()
    print("All Spend Times: {}".format(e - s))

