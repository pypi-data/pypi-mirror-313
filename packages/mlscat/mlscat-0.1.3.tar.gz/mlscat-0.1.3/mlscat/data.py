import numpy as np
from sklearn import preprocessing
import h5py

'''
This is a load data module.
'''


'''
load ascad,chesctf,DPAv42.et datasets
'''

def load_data(dataset_name, path) -> dict:
    '''
    ### load_data
    
    Args:
    `dataset_name`: dataset name like: ascad, chesctf.
    `path`: dataset's absolute path.

    Returns:
        data dict.

    Example:
    >>> result = load_data('ASCAD', '/home/xxx/ASCAD.h5')
    >>> result.keys()
    dict_keys(['profiling_traces', 'profiling_labels', 'profiling_plaintext', 'profiling_key', 'attack_traces', 'attack_labels', 'attack_plaintext', 'attack_key'])
    '''
    result = {}
    if str.lower(dataset_name) == 'ascad':
        with h5py.File(path, 'r') as hf:
            result['profiling_traces'] = np.array(hf['Profiling_traces/traces'], dtype=np.float32)
            result['profiling_labels'] = np.array(hf['Profiling_traces/labels'], dtype=np.float32)
            result['profiling_plaintext'] = np.array(hf['Profiling_traces/metadata'][:]['plaintext'], dtype=np.int16)
            result['profiling_key'] = np.array(hf['Profiling_traces/metadata'][:]['key'], dtype=np.int16)
            
            # Load attack traces
            result['attack_traces'] = np.array(hf['Attack_traces/traces'], dtype=np.float32)
            result['attack_labels'] = np.array(hf['Attack_traces/labels'], dtype=np.int16)
            result['attack_plaintext'] = np.array(hf['Attack_traces/metadata'][:]['plaintext'], dtype=np.int16)
            result['attack_key'] = np.array(hf['Attack_traces/metadata'][:]['key'], dtype=np.int16)
    return result

def minmax(x, y, data) -> np.ndarray:
    '''
    ### minmax
    
    `A function scale the data to x, y`
    
    Args:
    `x`: begain.
    `y`: end.
    `data`: scaled data.
    
    Returns:
        data array.
    '''

    scale = preprocessing.MinMaxScaler(feature_range=(x, y))
    scaled_data = scale.fit_transform(data)
    return scaled_data


def convert_bin_label(labels) -> np.ndarray:
    '''
    ### convert_bin_label   

    Args:
    `labels`: normal labels array.

    Returns:
        bin labels array.
        
    Examples:
    >>> convert_bin_label([10,2])
    array[[0. 0. 0. 0. 1. 0. 1. 0.]
          [0. 0. 0. 0. 0. 0. 1. 0.]]
    '''
    result = np.zeros(shape=(len(labels), 8))
    for index, label in enumerate(labels):
        bin_label = bin(int(label))[2:].zfill(8)
        bin_arr_label = [int(x) for x in bin_label]
        result[index] = bin_arr_label
    return result