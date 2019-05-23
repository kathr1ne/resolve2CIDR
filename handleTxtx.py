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
# country_codes = ['SG', 'US', 'TW', 'EU', 'JP', 'KR', 'RU', 'VN', 'AU']
country_codes = ['SG', 'TW', 'JP', 'KR', 'RU', 'VN', 'AU', 'EU', 'US']

# set colums names
# refer: https://github.com/ipipdotnet/ipdb-python
names = ['startIP', 'endIP', 'country_name', 'region_name', 'city_name', 'owner_domain', \
	 'isp_domain', 'latitude', 'longitude', 'timezone', 'utc_offset', 'china_admin_code', \
	 'idd_code', 'country_code', 'continent_code']

# read data; set dtype
s1 = time.time()
# data = pd.read_csv('mytestip.txtx', names=names, sep='\s+', dtype='category')
data = pd.read_csv('mydata4vipday2.txtx', names=names, sep='\s+', dtype='category')
e1 = time.time()
print 'e1s1 spend time {}s'.format(e1 - s1)

s2 = time.time()
data['startIP'] = data['startIP'].astype('object')
data['endIP'] = data['endIP'].astype('object')
e2 = time.time()
print 'e2s2 spend time {}s'.format(e2 - s2)
# 纳米比亚 国家两位代码位NA 与pandas默认空值冲突 清洗为NAM
# data['country_code'] = data['country_code'].cat.add_categories(['NAM']);
# data.country_code.fillna('NAM', inplace=True)

# change column order
# cols = list(data)
# cols.insert(2, cols.pop())
# print data[cols]

def filter_ccode(ccode):
    if ccode == 'EU':
	country_df = data[data['continent_code'] == ccode].copy()
    else:
	country_df = data[data['country_code'] == ccode].copy()
    # country_df['CIDR'] = country_df['startIP'] + '-' + country_df['endIP']
    # country_df['CIDR'] = country_df['CIDR'].map(function)

    # Capture ValueError
    # https://stackoverflow.com/questions/55321537/df-apply-valueerror-cannot-set-a-frame-with-no-defined-index-and-a-value-that
    try:
	country_df['CIDR'] = country_df.apply(lambda df: iprange_to_cidrs(df['startIP'], df['endIP']), axis=1)
    except ValueError:
	pass
    return country_df

for ccode in country_codes:
    l = []
    s3 = time.time()
    try:
	for i in filter_ccode(ccode)['CIDR'].values:
	    l.extend(i)
	l = cidr_merge(l)
	pd.Series(l).to_csv('result/setlist/{}.list'.format(ccode.lower()), index=False, header=False)
	e3 = time.time()
	print 'e3s3 {} spend time {}s'.format(ccode, e3 - s3)
    # Capture KeyError: 'CIDR'
    except KeyError:
	pass


'''
for ccode in country_codes:
    try:
	df = filter_ccode(ccode)['CIDR'].str.split(',', expand=True).stack()
	df = pd.Series(CIDR_IPSet(df))
    except IndexError:
	df = pd.Series([])
    df.to_csv('result/setlist/{}.list'.format(ccode.lower()), index=False, header=False)
'''
