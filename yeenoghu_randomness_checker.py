# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 17:36:13 2019

@author: Mangifera
"""

import seaborn as sns
import pandas as pd
from scipy import stats



def is_it_random(filename):
    with open(filename, "r") as text_file:
        demon = text_file.read()
        
    demon = [int(x) for x in demon.split('\n')]
    
    occurrence = {}
    
    for i in demon:
        if i in occurrence:
            occurrence[i] += 1
        else:
            occurrence[i] = 1
    
    occurrences = pd.DataFrame.from_dict(occurrence, orient = "index", columns=['rolls'])
    occurrences = occurrences.reset_index()
    occurrences = occurrences.rename(index=str, columns={"index": "die_side"})

    sns.set(style="whitegrid")
    ax = sns.barplot(x="die_side", y="rolls", data=occurrences)
    
#    chi2 = stats.chi2_contingency(occurrences["rolls"])
#    
#    chi_square_stat = chi2[0]
#    p_value = chi2[1]
#    degrees_of_freedom = chi2[2]
#    
#    print (chi_square_stat, p_value, degrees_of_freedom)


#is_it_random("yeenoghu.txt")
is_it_random("actual_data_yeenoghu.txt")

