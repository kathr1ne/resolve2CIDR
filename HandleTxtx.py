#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import time
import pandas as pd
from netaddr import iprange_to_cidrs
from netaddr import cidr_merge

"""
国家两位代码 - GRE
CN - eth0   # 大陆
HK - gre1   # default2HK
SG - gre2   # 新加坡
US - gre3   # 美国
TW - gre4   # 台湾省
EU - gre5   # 欧洲地区 对应txtx大洲代码
JP - gre6   # 日本
KR - gre7   # 韩国
RU - gre8   # 俄罗斯
VN - gre9   # 越南
AU - gre10  # 澳大利亚
-----------------------------------------------
refer: https://zh.wikipedia.org/wiki/ISO_3166-1
-----------------------------------------------
"""
country_codes = ['SG', 'TW', 'JP', 'KR', 'RU', 'VN', 'AU', 'EU', 'US']

# set colums names
# refer: https://github.com/ipipdotnet/ipdb-python
names = ['startIP', 'endIP', 'country_code', 'continent_code']

# read src data; set dtype
s1 = time.time()
data = pd.read_csv('mydata4vipday2.txtx', names=names, sep='\s+', dtype='category', usecols=[0, 1, 13, 14])
e1 = time.time()
print 'e1s1 [read_csv] spend time {}s'.format(e1 - s1)
data['startIP'] = data['startIP'].astype('object')
data['endIP'] = data['endIP'].astype('object')

def sort_by_ccode(ccode):
    s3 = time.time()
    if ccode == 'EU':
	df = data[data['continent_code'] == ccode].copy()
    else:
	df = data[data['country_code'] == ccode].copy()
    # Capture ValueError
    # https://stackoverflow.com/questions/55321537/df-apply-valueerror-cannot-set-a-frame-with-no-defined-index-and-a-value-that
    # try:
    #     df['CIDR'] = df.apply(lambda x: iprange_to_cidrs(x['startIP'], x['endIP']), axis=1)
    # except ValueError:
    #     pass
    # return df
    l = []
    for i in df.itertuples():
	cidr =  iprange_to_cidrs(i.startIP, i.endIP)
	l.extend(cidr)
    l = cidr_merge(l)
    e3 = time.time()
    print 'e3s3 {} [sort by ccode] spend time {}s'.format(ccode, e3 - s3)
    return l

for ccode in country_codes:
    try:
	# for i in sort_by_ccode(ccode).itertuples():
	#     l.extend(i.CIDR)
	# l = cidr_merge(l)
	# Write2File
	s4 = time.time()
	lists = [str(line) + '\n' for line in sort_by_ccode(ccode)]
	with open('result/setlist/{}.list'.format(ccode.lower()), 'w') as f:
	    f.writelines(lists)
	e4 = time.time()
	print 'e4s4 {} [write file] spend time {}s'.format(ccode, e4 - s4)
    # Capture KeyError: 'CIDR'
    except KeyError:
	pass
