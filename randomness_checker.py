# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 17:23:39 2019

@author: Mangifera
"""

from random import randint

def yeenoghu(no_dice_sides, no_of_dice):    
    return (randint(1, no_dice_sides) for _ in range(no_of_dice))


values = "\n".join(map(str, yeenoghu(20, 20000)))
print(values)

with open("yeenoghu_my_pc.txt", "w") as text_file:
    text_file.write(values)