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
    if s[0] == e[0]:
	if s[1] == e[1]:
	    for i in range(int(s[2]), int(e[2])):
		s[2] = str(i)
		s[3] = '0/24'
		CIDR.add(IP('.'.join(s)))
	    s[2] = e[2] #str(int(s[2]) + 1)
	    s[3] = '0'
	    try:
		CIDR.add(IP('{}-{}'.format('.'.join(s), '.'.join(e))))
		return CIDR
	    except Exception:
		CIDR.add(rangeIPd(e))
		return CIDR
	elif s[1] != e[1]:
	    print s, e
	    for i in range(int(s[1]), int(e[1])):
		s[1] = e[1] = str(i)
		CIDR.add(IP('{}-{}'.format('.'.join(s), '.'.join(e))))
	    print s, e
	    s[1] = e[1] = str(int(e[1]) + 1)
	    print s, e
	    CIDR.add(dealwithValueError('.'.join(s), '.'.join(e)))
	    return CIDR
    elif s[0] != e[0]:
	for i in range(int(s[0]), int(e[0])):
	    s[0] = str(i)
	    s[3] = '0/8'
	    CIDR.add(IP('.'.join(s)))
	s[0] = e[0]
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
    # tolastip = '2.13.0.0 - 2.15.255.255'
    # tolastip = '028.000.000.000-030.255.255.255'
    tolastip = '017.092.128.000-017.094.255.255'
    cidr = ['192.168.0.0/24', '192.168.1.0/24']
    print convert2CIDR(tolastip)
