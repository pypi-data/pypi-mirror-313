import numpy as np
from tqdm import tqdm
from .utils import get_mid, AES_Sbox
from .leakage import *

def dpa(traces, plaintexts, threshold, target_byte, target_point, leakage_function):
    """
    DPA

    `This function is just for AES-128, if attack AES-256 or others, plz change it.`

    Args:
        `traces`: an array of power consumption measurements.
        `plaintexts`: an array of plaintexts.
        `threshold`: an integer threshold value.
        `target_byte`: the target byte to attack.
        `target_point`: the target point in the traces to analyze.
        `leakage_function`: the leakage function to use (either 'hw' for Hamming weight or another function).

    Returns:
        `candidate`:after calculation get the maximum value.
        `mean_diffs`:after calculation get the mean_diffs.
    
    Case:
    >>> ### trace.shape = (2000, 15000), plaintext.shape = (2000, 16)
    >>> dpa(traces, plaintexts, threshold=4, target_byte=0, target_point=810, leakage_function='hw')
    """
    candidate_key = []
    maximum = 0
    mean_diffs = np.zeros(256)
    for i in tqdm(range(256)):
        traces_group1 = []
        traces_group2 = []
        for num in range(len(traces)):
            mid_val = hw(AES_Sbox[plaintexts[num][target_byte] ^ i]) if leakage_function.lower() == 'hw' else AES_Sbox[plaintexts[num][target_byte] ^ i]
            if mid_val < threshold:
                traces_group1.append(traces[num][target_point])
            else:
                traces_group2.append(traces[num][target_point])
        mean_diffs[i] = abs(np.mean(traces_group1) - np.mean(traces_group2))
        if mean_diffs[i] > maximum:
            maximum = mean_diffs[i]
            candidate_key = i
    return candidate_key, mean_diffs

def cpa(byte_idx, plaintexts, traces, mask_scheme=None, mask=-1)->np.ndarray:
    '''
    CPA 
    
    `A function to implement correlation power analysis.`
    
    Args:
        `byte_idx`: input the index of the key bytes you want to attack.
        `plaintexts`: input the plaintext array type is numpy arrary.
        `traces`: traces array just like plaintexts.
        `mask_scheme`: please input your mask scheme, TODO: this arg will be used in next version :)
        `mask`: input your mask list, shape = (1, n).
        
    Returns: 
        `ndarry`: return guess key list.
    
    Raises:
        for version 0.x, there does not have any raises, we do not check any inputs just give u a tips.
    Case:
        >>> guess_keys, data = cat.cpa(1, [[1],[2],[3],[4]], [[23], [44], [55], [77]], 'bool', mask=-1)
        
    > It is just a example, you need replace the plaintexts and traces to real data.
    '''
    traces_num = traces.shape[0]
    data = []
    for k in tqdm(range(256), desc="[+] byte: " + str(byte_idx)):
        targets = np.zeros(shape=(traces_num))
        for index in range(traces_num):
            targets[index] = get_mid(plaintexts[index][byte_idx], k, mask, mask_scheme)
        data.append(max(pcc(targets, traces)))
    guess_keys = np.argmax(data)
    return guess_keys

def pcc(targets:np.array, traces:np.array):
    '''
    ### Pearson correlation coeffcuent
    
    return abs value, whether it is positive or negative
    '''
    point_num = traces.shape[1]
    pearson_list = np.zeros(point_num)
    for num in range(point_num):
        pearson_list[num] = pearson(targets, traces[:, num])
    return pearson_list

def pearson(x:np.array, y:np.array):
    x = (x-np.mean(x,axis=0))/np.std(x,axis=0)
    x = x/np.linalg.norm(x,axis=0)
    y = (y-np.mean(y,axis=0))/np.std(y,axis=0)
    y = y/np.linalg.norm(y,axis=0)
    m = np.dot(x.T,y)
    return abs(m)

# signal-noise ratio
def prepare_data(trace_set, labels_set):
    labels=np.unique(labels_set)
    #initialize the dictionary
    d={}
    for i in labels:
         d[i]=[]
    for count, label in enumerate(labels_set):
        d[label].append(trace_set[count])
    return d



# link: https://ileanabuhan.github.io/general/2021/05/07/SNR-tutorial.html
def snr(trace_set, labels_set):
    mean_trace={}
    signal_trace=[]
    noise_trace=[]
    labels=np.unique(labels_set) 
    
    grouped_traces=prepare_data(trace_set, labels_set) 
    
    for i in labels:
        mean_trace[i]=np.mean(grouped_traces[i], axis=0)
        signal_trace.append(mean_trace[i]) 
    
    for i in labels:
        for trace in grouped_traces[i]:
            noise_trace.append(trace-mean_trace[i])
    var_noise=np.var(noise_trace, axis=0)
    var_signal=np.var(signal_trace, axis=0)
    snr_trace=var_signal/var_noise  
    return snr_trace   

