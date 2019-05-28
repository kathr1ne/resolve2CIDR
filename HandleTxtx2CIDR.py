#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import time
import pandas as pd
from netaddr import iprange_to_cidrs
from netaddr import cidr_merge

class Resolve2Cidr(object):
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
    def __init__(self, txtxfile, names, usecols):
	self.txtxfile = txtxfile
	self.names = names
	self.usecols = usecols

    @staticmethod
    def check_dir(basedir):
        """
	check save file dirs exists
	"""
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
	return src_dir, cn_src_dir

    def read_data(self):
	"""
	read src data and set dtype
	:return tuple (data, cn_data, province_array)
	"""
	s1 = time.time()
	data = pd.read_csv(self.txtxfile, names=self.names, usecols=self.usecols, sep='\s+', dtype='category')
	cn_data = data[data['country_code'] == 'CN'].copy()
	province_array = cn_data['region_name'].unique().get_values()
	e1 = time.time()
	print 'pandas [read_csv] spend time {}s'.format(e1 - s1)
	return data, cn_data, province_array

    def merge2cidr(self, dataframe, code):
	"""
	:param dataframe: pandas DataFrame
	:param code: code in global variable [country_codes]
	:return list after netaddr.cide_merge
	"""
        s2 = time.time()
        l = []
        for i in dataframe.itertuples():
	   cidr =  iprange_to_cidrs(i.startIP, i.endIP)
	   l.extend(cidr)
        l = cidr_merge(l)
        e2 = time.time()
        print '{} [merge2cidr] spend time {}s'.format(code, e2 - s2)
        return l

    def sort_by_country_code(self, code):
	"""
	iteration country_cedes
	:param code: code in global variable [country_codes]
	:return list after netaddr.cide_merge
	"""
        if code == 'EU':
	    dataframe = data[0][data[0]['continent_code'] == code].copy()
	else:
	    dataframe = data[0][data[0]['country_code'] == code].copy()
        return self.merge2cidr(dataframe, code)

    def sort_by_province(self, code):
	"""
	:param code: china province array
	:return list after netaddr.cide_merge
	"""
        dataframe = data[1][data[1]['region_name'] == code].copy()
        return self.merge2cidr(dataframe, code)

    def write_file(self, code, CN=None):
	if CN is None:
	    s3 = time.time()
	    lists = ['add {} {}{}'.format(code.lower(), str(line), '\n') for line in self.sort_by_country_code(code)]
	    with open('{}/{}.list'.format(dirs[0], code.lower()), 'w') as f:
	        f.writelines(lists)
	    e3 = time.time()
	    print '{} [write file] spend time {}s'.format(code, e3 - s3)
	    print '----------------'
	else:
	    s3 = time.time()
	    lists = [str(line) + '\n' for line in self.sort_by_province(code)]
	    with open('{}/{}.list'.format(dirs[1], code), 'w') as f:
		f.writelines(lists)
	    e3 = time.time()
	    print '{} [write file] spend time {}s'.format(code, e3 - s3)

if __name__ == '__main__':
    # workspace
    basedir = os.path.abspath(os.path.dirname(__file__))
    dirs = Resolve2Cidr.check_dir(basedir)
    # country_codes U need
    country_codes = ['CN', 'SG', 'TW', 'JP', 'KR', 'RU', 'VN', 'AU', 'TH', 'IN', 'EU', 'CA', 'US']
    # set colums names && usecols refer: https://github.com/ipipdotnet/ipdb-python
    names = ['startIP', 'endIP', 'country_name', 'region_name', 'country_code', 'continent_code']
    usecols = [0, 1, 2, 3, 13, 14]
    txtx_file = os.path.join(basedir, 'mydata4vipday2.txtx')
    # Instantiation
    obj = Resolve2Cidr(txtx_file, names, usecols)
    data = obj.read_data()
    for code in country_codes:
	obj.write_file(code)
    for code in data[2]:
	obj.write_file(code, CN=True)
