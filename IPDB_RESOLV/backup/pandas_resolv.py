#!/usr/bin/env python
#
#


import ipdb
import pandas as pd
from time import time
from netaddr import IPNetwork
from netaddr import cidr_merge
from netaddr import iprange_to_cidrs


def read_data(range_cidr):
    s = time()
    data = pd.DataFrame()
    ip = IPNetwork(range_cidr)
    for i in ip:
        dic = db.find_map(i, 'CN')
        dic['IP'] = i
        d = pd.DataFrame(dic, index=[0])
        data = data.append(d)
    e = time()
    print("[read_data] time: {}".format(e - s))
    return data

def get_dataframe(data, code):
    s = time()
    dataframe = data[data['country_code'].isin([code])].copy()
    e = time()
    print("[get_dataframe] time: {}".format(e - s))
    return dataframe

def merge_to_cidr(dataframe):
    s = time()
    l = dataframe.IP.values.tolist()
    cidr = cidr_merge(l)
    e = time()
    print("[merge_to_cidr] time: {}".format(e - s))
    return cidr


country_codes = ['CN', 'SG', 'TW', 'JP', 'KR', 'RU', 'VN', 'AU', 'TH', 'IN', 'EU', 'CA', 'US']
db = ipdb.City("/home/kongs/resolve2CIDR/mydata4vipday2.ipdb")

# range_cidr = '8.253.128.0/17'
range_cidr = '1.0.0.0/8'
data = read_data(range_cidr)

for code in country_codes:
    dataframe = get_dataframe(data, code)
    cidr = merge_to_cidr(dataframe)
    print(code, cidr)
    print("======================")

