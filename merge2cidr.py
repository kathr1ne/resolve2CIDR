#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import pandas as pd
from netaddr import iprange_to_cidrs
from netaddr import cidr_merge
from HandleTxtx import Resolve2Cidr


class TestClass(Resolve2Cidr):
    def __init__(self, txtxfile, names, usecols):
        self.txtxfile = txtxfile
        self.names = names
        self.usecols = usecols

    def merge2cidr(self, dataframe):
        l = []
        l_extend = l.extend
        for i in dataframe.itertuples():
            cidr = iprange_to_cidrs(i.startIP, i.endIP)
            l_extend(cidr)
        l = cidr_merge(l)
        return l


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    country_codes = ['TENCENT.COM']
    names = [
        'startIP',
        'endIP',
        'country_name',
        'region_name',
        'country_code',
        'continent_code']
    usecols = [0, 1, 2, 3, 13, 14]
    txtx_file = os.path.join(basedir, 'merge2cidr.txtx')
    obj = TestClass(txtx_file, names, usecols)
    data = obj.read_data()
    for i in obj.merge2cidr(data[0]):
        print(i)
    
