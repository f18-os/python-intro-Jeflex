# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 12:49:13 2018

@author: Phillip
"""

import sys       
import re         
import os         
import subprocess 

while(1):
    sys.stdout.write(os.curdir + ':$')
    data = str(sys.stdin.readline().strip('\n').split(' '))
    
    if 'exit' in data:
        sys.stdout.flush
        break
    
    sys.stdout.write('Parent pid = '+str(os.getpid()))
    
    
    #if '>' in data:
        
    #if '<' in data:
    
    #if '|' in data:
    
    newPid = os.fork()
    if newPid == 0:
        os.close
    else:
        os.waitpid(newPid)
        os.execv(data[0],data[1:])
    
    sys.stdout.write('\n')
    sys.stdout.flush
    