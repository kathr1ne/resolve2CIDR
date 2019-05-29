#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging

def set_log(log_file):
    logging.basicConfig(level=logging.INFO,
                format = '%(asctime)s %(filename)s[%(lineno)d]: %(levelname)s %(message)s',
                datefmt = '%F %T',
                filename = log_file,
                filemode = 'w')
