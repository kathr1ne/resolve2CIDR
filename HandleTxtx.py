#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import time
import pandas as pd
from netaddr import iprange_to_cidrs
from netaddr import cidr_merge

# workspace
basedir = os.path.abspath(os.path.dirname(__file__))

# check dir
result_dir = os.path.join(basedir, 'result')
src_dir = os.path.join(result_dir, 'setlist')
cn_src_dir = os.path.join(result_dir, 'cnsetlist')
if not os.path.exists(result_dir):
    os.mkdir(result_dir)	
    os.mkdir(src_dir)
    os.mkdir(cn_src_dir)
else:
    if not os.path.exists(src_dir):
        os.mkdir(src_dir)
    if not os.path.exists(cn_src_dir):
        os.mkdir(cn_src_dir)

"""
国家两位代码 - GRE
CN - eth0   # 大陆 set eth0 out
HK - gre1   # default2HK
SG - gre2   # 新加坡
US - gre3   # 美国
CA - gre3   # 加拿大
TW - gre4   # 台湾省
EU - gre5   # 欧洲地区 对应txtx大洲代码
JP - gre6   # 日本
KR - gre7   # 韩国
RU - gre8   # 俄罗斯
VN - gre9   # 越南
AU - gre10  # 澳大利亚
TH  # 泰国
IN  # 印度
-----------------------------------------------
refer: https://zh.wikipedia.org/wiki/ISO_3166-1
-----------------------------------------------
"""
country_codes = ['CN', 'SG', 'TW', 'JP', 'KR', 'RU', 'VN', 'AU', 'TH', 'IN', 'EU', 'CA', 'US']

# set colums names
# refer: https://github.com/ipipdotnet/ipdb-python
names = ['startIP', 'endIP', 'country_name', 'region_name', 'country_code', 'continent_code']

# read src data; set dtype
s1 = time.time()
data_file = os.path.join(basedir, 'mydata4vipday2.txtx')
data = pd.read_csv(data_file, names=names, sep='\s+', dtype='category', usecols=[0, 1, 2, 3, 13, 14])
cn_data = data[data['country_code'] == 'CN'].copy()
provice_array = cn_data['region_name'].unique().get_values()
e1 = time.time()
print 'e1s1 [read_csv] spend time {}s'.format(e1 - s1)

def merge2cidr(df):
    s3 = time.time()
    l = []
    for i in df.itertuples():
	cidr =  iprange_to_cidrs(i.startIP, i.endIP)
	l.extend(cidr)
    l = cidr_merge(l)
    e3 = time.time()
    print 'e3s3 {} [merge2cidr] spend time {}s'.format(ccode, e3 - s3)
    return l

def sort_by_ccode(ccode):
    if ccode == 'EU':
	df = data[data['continent_code'] == ccode].copy()
    else:
	df = data[data['country_code'] == ccode].copy()
    return merge2cidr(df)

def sort_by_provice(provice):
    df = cn_data[cn_data['region_name'] == provice].copy()
    return merge2cidr(df)

for ccode in country_codes:
    s4 = time.time()
    lists = ['add {} {}{}'.format(ccode.lower(), str(line), '\n') for line in sort_by_ccode(ccode)]
    with open('{}/{}.list'.format(src_dir, ccode.lower()), 'w') as f:
        f.writelines(lists)
    e4 = time.time()
    print 'e4s4 {} [write file] spend time {}s'.format(ccode, e4 - s4)

for ccode in provice_array:
    s4 = time.time()
    lists = [str(line) + '\n' for line in sort_by_provice(ccode)]
    with open('{}/{}.list'.format(cn_src_dir, ccode), 'w') as f:
	f.writelines(lists)
    e4 = time.time()
    print 'e4s4 {} [write file] spend time {}s'.format(ccode, e4 - s4)
