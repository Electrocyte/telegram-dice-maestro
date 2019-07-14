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
    
    return occurrence
    

def make_df(filename_ctrl, filename_sample):
#    occurrence_ctrl = is_it_random(filename_ctrl)
#    occurrences_ctrl = pd.DataFrame.from_dict(occurrence_ctrl, orient = "index", columns=['rolls_ctrl'])
#    occurrences_ctrl = occurrences_ctrl.reset_index()
#    occurrences_ctrl = occurrences_ctrl.rename(index=str, columns={"index": "die_side"})
    
    occurrence_samp = is_it_random(filename_sample)
    occurrences_samp = pd.DataFrame.from_dict(occurrence_samp, orient = "index", columns=['rolls_samp'])
    occurrences_samp = occurrences_samp.reset_index()
    occurrences_samp = occurrences_samp.rename(index=str, columns={"index": "die_side"})
    
#    occurrences = pd.merge(occurrences_ctrl, occurrences_samp, on='die_side')
    max_die_no = max(occurrences_samp['die_side'])
    total_rolls = sum(occurrence_samp.values())
    uniform_prediction = total_rolls/max_die_no
    
    occurrences = occurrences_samp.set_index("die_side")
      
    occurrences['uniform_dist'] = pd.Series(uniform_prediction, index=occurrences.index)

    sns.set(style="whitegrid")
    ax = sns.barplot(x=occurrences.index, y="rolls_samp", data=occurrences)
    
    chi2 = stats.chi2_contingency(occurrences)
    
    chi_square_stat = chi2[0]
    p_value = chi2[1]
    degrees_of_freedom = chi2[2]
    
    print (f"chi_square_stat: {chi_square_stat}, p-value: {p_value}, degrees_of_freedom: {degrees_of_freedom}")


filename_sample = "actual_data_yeenoghu.txt"
filename_ctrl = "yeenoghu_my_pc.txt"

z = make_df(filename_ctrl, filename_sample)