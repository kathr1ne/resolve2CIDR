#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import time
import pandas as pd
from netaddr import iprange_to_cidrs
from netaddr import cidr_merge
from netaddr import IPSet

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

def filter_ccode(ccode):
    if ccode == 'EU':
	country_df = data[data['continent_code'] == ccode].copy()
    else:
	country_df = data[data['country_code'] == ccode].copy()
    # Capture ValueError
    # https://stackoverflow.com/questions/55321537/df-apply-valueerror-cannot-set-a-frame-with-no-defined-index-and-a-value-that
    try:
        country_df['CIDR'] = country_df.apply(lambda df: iprange_to_cidrs(df['startIP'], df['endIP']), axis=1)
    except ValueError:
        pass
    return country_df
    # return [IPSet(iprange_to_cidrs(i.startIP, i.endIP)) for i in country_df.itertuples()]

for ccode in country_codes:
    l = []
    # s = IPSet()
    s3 = time.time()
    try:
	for i in filter_ccode(ccode).itertuples():
	    l.extend(i.CIDR)
	    # s = s.union(IPSet(i))
	l = cidr_merge(l)
	# 瓶颈 花费极大部分时间循环union CIDR
	# for i in filter_ccode(ccode):
	#     s = s.union(i)
	e3 = time.time()
	print 'e3s3 {} [filter country code] spend time {}s'.format(ccode, e3 - s3)

	# Write2File
	s4 = time.time()
	# pd.Series(list(s._cidrs)).to_csv('result/setlist/{}.list'.format(ccode.lower()), index=False, header=False)
	pd.Series(l).to_csv('result/setlist/{}.list'.format(ccode.lower()), index=False, header=False)
	e4 = time.time()
	print 'e4s4 {} [write file|to_csv] spend time {}s'.format(ccode, e4 - s4)
    # Capture KeyError: 'CIDR'
    except KeyError:
	pass
