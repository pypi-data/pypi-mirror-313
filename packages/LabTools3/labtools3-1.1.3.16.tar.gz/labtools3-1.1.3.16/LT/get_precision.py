#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:46:31 2018

@author: boeglinw
"""
import re

def get_colnumbers(d):
    # get the formats
    fmt = re.findall(d.F,d.headerline)
    col = []
    for f in fmt:
        c = int(f.split(',')[-1])
        col.append(c)
    return col

