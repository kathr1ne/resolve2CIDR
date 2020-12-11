#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


import ipdb
import threading
import pandas as pd
from netaddr import IPNetwork
from time import time


def resolve_ipdb(ip, index):
    for i in ip:
        r = db.find(i, 'CN')
        r = [str(i), r[0], r[1], r[-2], r[-1]]
        dic[index].append((' '.join(r) + '\n'))
    
    with open('./resolve_ipdb.txtx', 'a+') as f:
        f.writelines(dic[index])
    

db = ipdb.City("/home/kongs/resolve2CIDR/mydata4vipday2.ipdb")


dic = {}
for i in range(1, 224):
    s = time()
    dic[i] = []
    ip = IPNetwork('{}.0.0.0/8'.format(i))
    resolve_ipdb(ip, i)
    e = time()
    print("Finished. CIDR-{}.0.0.0/20 speed time: {}s".format(i, e - s))

