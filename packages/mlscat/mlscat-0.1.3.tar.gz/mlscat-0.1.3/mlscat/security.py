#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
* File       : security.py
* Created    : 2024-04-25 11:44:57
* Author     : M0nk3y
'''

import numpy as np
import random
import copy

def desynchronization(traces, window) -> np.ndarray:
    '''
    # Desynchronization
    `return traces with random delay`
    
    Args:
        `traces`: 2D origin traces, shape=(m, n).
        `window`: level of the delay distance.
    
    Returns:
        delay traces array
        
    Reminder:
        Default value zero padding
    '''
    delay_traces = np.zeros(shape=(traces.shape))
    for index, trace in enumerate(traces):
        random_num = random.randint(0, window)
        if random_num != 0:
            delay_traces[index][random_num:] = trace[:-random_num]
        else:
            delay_traces[index] = trace
    return delay_traces

def add_gaussian_noise(traces, std, mean=0):
    """
    # add_gaussian_noise
    
    `traces`: origin traces.
    `std` : standard deviation, control the noise level
    `mean`: mean value.
    
    Returns:
        traces array with noise.
    """
    noise_traces = np.zeros(shape=traces.shape)
    for index, trace in enumerate(traces):
        noise = np.random.normal(mean, std, len(trace)).astype(dtype=np.float32)
        noise_traces[index] = trace + noise
    return noise_traces

def shuffling(traces, times):
    """
    # Shuffling
    
    Can only Simulate random shuffling
    
    Args:
        `traces`: origin traces.
        `times`: shuffling times.
        
    Returns:
        shuffled traces array.
    """
    
    shuffled_traces = copy.deepcopy(traces)
    for index, trace in enumerate(shuffled_traces):
        for i in range(times):
            random_nums = np.random.randint(0, len(trace), (2, ))
            temp_point = trace[random_nums[0]]
            trace[random_nums[0]] = trace[random_nums[1]]
            trace[random_nums[1]] = temp_point
        shuffled_traces[index] = trace
    return shuffled_traces