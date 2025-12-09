#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 15:42:16 2022

@author: anton
"""

import os
import sys
from time import time

t_start = time()
errorLog = []
doneLog = {}
paths = os.listdir('./')
for pathName in paths:
    mainFileName = pathName.split('/')[-1]
    if not os.path.isfile(pathName):
        os.chdir(pathName)
        files = os.listdir('./')
        if mainFileName + '.py' in files:
            try:
                print('\nExecuting:', mainFileName)
                t_begin = time()
                exec(open(mainFileName +'.py').read())
                t_end = time()
                print('\n', mainFileName, 'Total time:', t_end-t_begin, 's')
                doneLog[mainFileName] = t_end-t_begin
            except BaseException:
                exc_type, value, exc_traceback = sys.exc_info()
                print('\n', value)
                errorLog.append(mainFileName)
        else:
            print("ERROR: could not find:", mainFileName)
        os.chdir('../')
t_stop = time()
print('\nTotal test time:', t_stop-t_start, 's')
print("\nERRORS found in:")
print(errorLog)
print("\nPROCESSED:")
for key in list(doneLog.keys()):
    print(key, doneLog[key], 's')