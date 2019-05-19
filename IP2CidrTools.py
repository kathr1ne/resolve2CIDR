#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from IPy import IP
from IPy import IPSet

def dealwithValueError(start, end):
    """
    deal with IPy[IP('start-end')] ValueError
    start: CIDR start IP
    end: CIDR end IP   
    """
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
	    CIDR.add(rangeIPd(e))
	    return CIDR
    elif s[1] != e[1]:
	for i in range(256):
	    s[2] = str(i)
	    s[3] = '0/24'
	    CIDR.add(IP('.'.join(s)))
	s[1] = e[1]
	s[2] = s[3] = '0'
	CIDR.add(dealwithValueError('.'.join(s), '.'.join(e)))
	return CIDR

def rangeIPd(end):
    """
    range IP.d [a.b.c.d]
    """
    CIDR = IPSet()
    for i in range(int(end[3]) + 1):
	end[3] = str(i)
	CIDR.add(IP('.'.join(end)))
    return CIDR

def convert2CIDR(args, args_type='tolastip'):
    """
    convert -lastip to CIDR(/prefix)
    convert CIDR to big CIDR
    if arge type is -lastip: x.x.x.x-y.y.y.y
    if arge type is cidr: be list
    """
    if args_type is 'tolastip':
        try:
	   return IP(args).strNormal()
	   # CIDR = IPSet()
	   # CIDR.add(IP(args))
	   # return CIDR
        except Exception:
	   startIP = args.split('-')[0]
	   endIP = args.split('-')[1]
	   return ','.join([cidr.strNormal() for cidr in dealwithValueError(startIP, endIP)])
	   # return dealwithValueError(startIP, endIP)
    elif args_type is 'cidr':
	CIDR = IPSet()
	for cidr in args:
	    CIDR.add(IP(cidr))
	return CIDR
    else:
	return 'error args type, only support [tolastip|cidr]'

if __name__ == '__main__':
    # tolastip = '192.168.0.0-192.168.0.255'
    tolastip = '2.13.0.0 - 2.14.255.255'
    cidr = ['192.168.0.0/24', '192.168.1.0/24']
    print convert2CIDR(cidr, 'cidr')
