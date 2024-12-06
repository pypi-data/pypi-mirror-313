import numpy as np
import random
from sklearn.utils import shuffle

def calc_ge_sr(predictions, targets, num_traces, key, times=1000, interval=1):
    """
    Calculate the success rate and rank of a key in a given set of predictions and targets.

    Args:
        `predictions (list)`: A list of dictionaries representing the predictions for each target.
        `targets (numpy.ndarray)`: A 2D numpy array of shape (n, 256) representing the targets.
        `num_traces (int)`: The number of traces to consider.
        `key (int)`: The key to calculate the success rate and rank for.
        `times (int, optional)`: The number of times to run the calculation. Defaults to 1000.
        `interval (int, optional)`: The interval between traces. Defaults to 1.

    Returns:
        tuple: A tuple containing the success rate and rank of the key.
        
            - `success_rate (numpy.ndarray)`: An array of shape (n_i,) representing the success rate for each interval.
            - `all_keys_rank (numpy.ndarray)`: An array of shape (n_i,) representing the rank of the key for each interval.
    """
    all_predictions_probs = np.zeros((targets.shape[0], 256))
    n_i = int(num_traces / interval)
    all_keys_rank = np.zeros(n_i)
    success_rate = np.zeros(n_i)
    
    shuffled_index = np.random.permutation(len(predictions))[:num_traces]
    
    for index, prediction in enumerate(predictions):
        for k in range(256):
            all_predictions_probs[index, k] = prediction[targets[index, k]]
    for _ in range(times):
        shuffled_probs = all_predictions_probs[shuffled_index]
        shuffled_keys = key[shuffled_index]
        element_index = 0
        key_probs = np.zeros(256)
        for j in range(num_traces):
            key_probs += shuffled_probs[j]
            key_probs_sorted = np.argsort(key_probs)[::-1]
            if (j+1) % interval == 0:
                key_rank = list(key_probs_sorted).index(shuffled_keys)
                all_keys_rank[element_index] += key_rank
                if key_rank <= 1:
                    success_rate[element_index] += 1
                element_index += 1
                
    return success_rate / times, all_keys_rank / times

def mutual_information(predictions, y):
    '''
    ### MutualInformation
    `cal mutual information `
    
    Args:
    
    `predictions`: input your model.predict(x).
    `y`: input your x corresponding labels.

    Returns:
    MI
    '''
    
    pass

def perceived_information():
    pass