#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


import os
import pandas as pd
import multiprocessing
from netaddr import cidr_merge
from time import time


def read_data(txtxfile):
    s = time()
    # names = ['IP', 'country_name', 'region_name', 'country_code', 'continent_code']
    names = ['IP', 'country_name', 'country_code', 'continent_code']
    data = pd.read_csv(txtxfile, names=names, sep=r'\s+', dtype='category')
    cn_data = data[data['country_code'].isin(['CN'])].copy()
    e = time()
    print('[Read_csv File: {}] spend time {:.2f}s'.format(txtxfile.split('/')[-1], e - s))
    return data, cn_data

def merge_to_cidr(data, code):
    s = time()
    # EU Special
    if code == 'EU':
        dataframe = data[data['continent_code'].isin([code])].copy()
        dataframe = dataframe[True ^ dataframe['country_code'].isin(['RU'])]
    else:
        dataframe = data[data['country_code'].isin([code])].copy()
    l = dataframe.IP.values.tolist()
    cidr = cidr_merge(l)
    e = time()
    print("[Merge_To_CIDR: {}] time: {:.2f}".format(code, e - s))
    return cidr


def write_file(country_codes, index):
    # txtx_file = os.path.join(basedir, 'txtx', 'ip_data_{}.txtx'.format(str(index).zfill(3)))
    txtx_file = os.path.join('/data/resolve_result/txtx', 'ip_data_{}.txtx'.format(str(index).zfill(3)))
    try:
        data = read_data(txtx_file)
    except FileNotFoundError as e:
        print('Except Error: {}'.format(e))
        return False
    for code in country_codes:
        cidr = merge_to_cidr(data[0], code)
        lists = [str(line) + '\n' for line in cidr]
        # save_name = os.path.join(basedir, 'setlist', '{}_temp.set'.format(code.lower()))
        save_name = os.path.join('/data/resolve_result/setlist', '{}_temp.set'.format(code.lower()))
        with open(save_name, 'a') as ipset_file:
            ipset_file.writelines(lists)

def multi_process(start, end):
    procs = []
    end = start + step
    for i in range(start, end):
        p = multiprocessing.Process(target=write_file, args=(country_codes, i))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    return True

def clean_temp(code):
    # temp_name = os.path.join(basedir, 'setlist', '{}_temp.set'.format(code.lower()))
    temp_name = os.path.join('/data/resolve_result/setlist', '{}_temp.set'.format(code.lower()))
    save_name = temp_name.replace('_temp', '')
    with open(temp_name, 'r') as temp_file:
        l = temp_file.readlines()
    cidr = cidr_merge(l)
    lists = [str(line) + '\n' for line in cidr]
    with open(save_name, 'a') as ipset_file:
        ipset_file.writelines(lists)
    if os.path.exists(temp_name):
        os.remove(temp_name)


if __name__ == '__main__':
    s = time()
    # basedir = os.path.abspath(os.path.dirname(__file__))
    country_codes = ['CN', 'SG', 'TW', 'JP', 'KR', 'RU', 'VN', 'AU', 'TH', 'IN', 'EU', 'CA', 'US']
    i = 0
    step = 16
    result = multi_process(i, step)
    while True:
        i += step
        if i == 256:
            break
        result = multi_process(i, step)
    # MERGE ALL
    for code in country_codes:
        clean_temp(code)
    e = time()
    print("Spend All Time: {}s".format(e - s))

