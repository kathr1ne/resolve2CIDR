#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pandas as pd
from IP2CidrTools import convert2CIDR
from IPy import IP
from IPy import IPSet

"""
国家两位代码 - GRE
CN - eth0   # 大陆
HK - gre1   # Default2HK
SG - gre2   # 新加坡
US - gre3   # 美国
TW - gre4   # 台湾
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
country_codes = ['SG', 'US', 'TW', 'EU', 'JP', 'KR', 'RU', 'VN', 'AU']

# set colums names
# refer: https://github.com/ipipdotnet/ipdb-python
names = ['startIP', 'endIP', 'country_name', 'region_name', 'city_name', 'owner_domain', \
	 'isp_domain', 'latitude', 'longitude', 'timezone', 'utc_offset', 'china_admin_code', \
	 'idd_code', 'country_code', 'continent_code']

# read data; set dtype
data = pd.read_csv('mytestip.txtx', names=names, sep='\s+', dtype='category')
data['startIP'] = data['startIP'].astype('object')
data['endIP'] = data['endIP'].astype('object')
# 纳米比亚 国家两位代码位NA 与pandas默认空值冲突 清洗为NAM
# data['country_code'] = data['country_code'].cat.add_categories(['NAM']);
# data.country_code.fillna('NAM', inplace=True)

# change column order
# cols = list(data)
# cols.insert(2, cols.pop())
# print data[cols]

def generate_df(ccode):
    if ccode == 'EU':
	country_df = data[data['continent_code'] == ccode].copy()
    else:
	country_df = data[data['country_code'] == ccode].copy()
    country_df['CIDR'] = country_df['startIP'] + '-' + country_df['endIP']
    country_df['CIDR'] = country_df['CIDR'].map(convert2CIDR)
    return country_df

def CIDR_IPSet(df):
    CIDR = IPSet()
    for i in df.iteritems():
	CIDR.add(IP(i[1]))
    return [cidr.strNormal() for cidr in CIDR]

for ccode in country_codes:
    try:
	df = generate_df(ccode)['CIDR'].str.split(',', expand=True).stack()
	df = pd.Series(CIDR_IPSet(df))
    except IndexError:
	df = pd.Series([])
    df.to_csv('result/setlist/{}.list'.format(ccode.lower()), index=False, header=False)
