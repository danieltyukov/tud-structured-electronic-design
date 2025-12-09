#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SLiCAP as sl
from time import time
t1 = time()
sl.initProject('Chapter 11')

import transimpedance
import simpleQamp
import RL1_0
import RL1_R
import RL1_L
import RL2_0
import RL2_1
import RL3_0
import RL3_1
import RL3_2
t2 = time()
print(t2-t1, 's')