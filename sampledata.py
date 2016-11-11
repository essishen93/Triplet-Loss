#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------
# TRIPLET LOSS
# Copyright (c) 2015 Pinguo Tech.
# Written by David Lu
# --------------------------------------------------------

import os
import codecs

class sampledata():

    global _sample_commodity
    global _sample_negative
    global _sample
    global _sample_label
    

    def __init__(self):
        self._sample_commodity = {}
        self._sample_negative = {}
        self._sample = []
        self._sample_label = {}
        lines = open('../data/train_1280.txt','r')
        for line in lines:
            comm_type = line.split('/')[0]
            picname = line.split(' ')[0]
            self._sample.append(picname)
            if comm_type in self._sample_commodity.keys():
                self._sample_commodity[comm_type].append(picname)
            else:
                self._sample_commodity[comm_type] = []
                self._sample_commodity[comm_type].append(picname)
            self._sample_label[comm_type] = int(line.split(' ')[1])
        print len(self._sample_commodity)

if __name__ == '__main__':

    sample = sampledata()
    #print sample._sample
