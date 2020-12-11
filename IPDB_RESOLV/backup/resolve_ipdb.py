#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


import csv
import ipdb
import multiprocessing
from netaddr import IPNetwork
from time import time


def resolve_ipdb(ip, index):
    s = time()    
    print("Start: Thread-{}".format(index))
    for i in ip:
        r = db.find(i, 'CN')
        r = [str(i), r[0], r[1], r[-2], r[-1]]
        dic[index].append((' '.join(r)))
    e = time()
    print("Finished: Thread-{} speed time {}s".format(index, e - s))

    with open('data01.csv', 'a+') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in dic[index]:
             spamwriter.writerow(i.split())
    

def multi_process(start, end):
    procs = []
    for i in range(start, end):
        dic[i] = []
        ip = IPNetwork('{}.0.0.0/12'.format(i))
        p = multiprocessing.Process(target=resolve_ipdb, args=(ip, i))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    return multiprocessing.active_children()
    

if __name__ == '__main__':
    db = ipdb.City("/home/kongs/resolve2CIDR/mydata4vipday2.ipdb")
    dic = {}
    start = 1
    end = 17
    result = multi_process(start, end)
            
