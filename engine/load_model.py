#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Julius Susanto. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
Load Model Library

Author: Julius Susanto
Last edited: November 2017
"""
import numpy as np

def create_loads(l_sum, l_win, sigma_s, sigma_w, hemi):
    """
    Creates a load profile with distinct summer and winter variations
    
    Inputs: 
        l_sum   Average hourly load profile for Summer (kW)
        l_win   Average hourly load profile for Winter (kW)
        sigma_s Standard deviation for Summer load profile
        sigma_w Standard deviation for Winter load profile
        hemi    Northern or Southern hemisphere
    
    Outputs:
        L_h     Hourly load profile for the year
    """
    
    L_h = []
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Swap seasons if in northern hemisphere
    if hemi == 'North':
        l_sum1 = l_sum
        l_sum = l_win
        l_win = l_sum1
    
    for i in range(12):
        for j in range(days[i]):
            if (i < 4) or (i > 9):  
                # Summer
                L_h.append(l_sum + sigma_s * np.random.randn(24))
            else:
                # Winter
                L_h.append(l_win + sigma_w * np.random.randn(24))   
        
    return np.ravel(L_h)