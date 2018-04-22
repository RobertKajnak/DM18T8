#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 14:51:48 2018

@author: edoardoguerriero
"""
import pandas as pd
import numpy as np

'''Tables with time aggregation of all variables except mood'''

n_patients = 23
id_patients = ['patient%d.csv' %i for i in range(n_patients)]

for patient in range(n_patients):
    
    '''Load files'''    
    name_file = id_patients[patient]
    df = pd.read_csv(name_file, delimiter=',')
    
    '''define time_scale, i.e. number of days for which we
       want to compute the average'''
    time_scale = 5
    
    '''define matrix to store the new dataset'''
    final_rows_num = df.shape[0] - time_scale
    columns = list(df)
    columns_num = df.shape[1]
    matrix = np.zeros((final_rows_num, columns_num))
    
    '''create the new dataset'''
    for col in range(columns_num):
        
        col_name = columns[col]
        
        for row in range(final_rows_num):
            
            '''the mood remain the same of the original dataset'''
            if col_name == 'mood':
                
                matrix[row][col] = int(df['mood'][row+time_scale]*10)
                '''mean of the other variables'''    
            else:
                
                matrix[row][col] =  np.mean(df[col_name][row:row+time_scale])
        
        if (max(matrix.T[col])- min(matrix.T[col])) != 0:
            
            matrix.T[col] = np.floor((matrix.T[col] - min(matrix.T[col]))/ \
                    (max(matrix.T[col])- min(matrix.T[col]))*100)
        else: 
            matrix.T[col] = matrix.T[col]*0
            
    '''convert matrix in pandas dataframe and save it'''    
    df_new = pd.DataFrame(matrix)   
    df_new.to_csv('patient%d_new_table_discr.csv' %patient)
