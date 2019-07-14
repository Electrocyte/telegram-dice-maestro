# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 17:36:13 2019

@author: Mangifera
"""

with open("yeenoghu.txt", "r") as text_file:
    demon = text_file.read()
    
demon = [int(x) for x in demon.split('\n')]

occurrence = {}

for i in demon:
    if i in occurrence:
        occurrence[i] += 1
    else:
        occurrence[i] = 1
