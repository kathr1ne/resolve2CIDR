#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from IPy import IP
from IPy import IPSet

def DealwithValueError(start, end):
    CIDR = IPSet()
    s = start.split('.')
    e = end.split('.')
    if s[1] == e[1]:
	for i in range(int(s[2]), int(e[2])):
	    s[2] = str(i)
	    s[3] = '0/24'
	    CIDR.add(IP('.'.join(s)))
	s[2] = str(int(s[2]) + 1)
	s[3] = '0'
	try:
	    CIDR.add(IP('{}-{}'.format('.'.join(s), '.'.join(e))))
	    return CIDR
	except Exception:
	    CIDR.add(DealwithValueError2(e))
	    return CIDR
    elif s[1] != e[1]:
	for i in range(256):
	    s[2] = str(i)
	    s[3] = '0/24'
	    CIDR.add(IP('.'.join(s)))
	s[1] = e[1]
	s[2] = s[3] = '0'
	CIDR.add(DealwithValueError('.'.join(s), '.'.join(e)))
	return CIDR

def DealwithValueError2(end):
    CIDR = IPSet()
    for i in range(int(end[3]) + 1):
	end[3] = str(i)
	CIDR.add(IP('.'.join(end)))
    return CIDR

country = set()
with open('/root/IPIP/mytestip.txtx', 'r') as f:
    for line in f:
	l = line.split()
	country.add(l[3])	
	try:
	    ip = IP('{}-{}'.format(l[0], l[1]))
	    print ip
	except Exception as error:
	    print DealwithValueError(l[0], l[1])
