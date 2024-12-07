import numpy as np
import pandas as pd
import mne
import matlab.engine
import os
import warnings
from scipy.signal import detrend

warnings.filterwarnings("ignore", category=RuntimeWarning)

def LZ78(X):
    """
    Compute LZ78 complexity of univariate time signal X using a standard
    word-dictionary algorithm.

    Inputs:
        X -- 1D array with real-valued signal

    Outputs:
        c -- raw (unnormalised) value of LZ78 complexity (i.e., dictionary length)
    """
    if len(X.shape) > 1 and X.shape[1] > 1:
        raise ValueError("Input array must be 1D")

    v = (detrend(X) > 0).astype(int)
    s = ''.join(map(str, v))

    dictionary = {}
    w = ""

    for ch in s:
        w += ch
        if w not in dictionary:
            dictionary[w] = True
            w = ""

    c = len(dictionary)
    return c

def process_LZ78(original_set_path, processed_set_path, epoch_length, custom_channel_groups=None):
    """
    Processes an EEG '.set' file to compute LZc and LZsum metrics,
    maps them to their original epoch positions using MATLAB-generated ogpath,
    and returns DataFrames with computed values and gaps.

    Parameters:
    - original_set_path (str): Path to the original '.set' EEG file.
    - processed_set_path (str): Path to the processed '.set' EEG file.
    - epoch_length (str): Description of epoch length (e.g., '4secs').
    - custom_channel_groups (dict, optional): Custom channel groupings.

    Returns:
    - dict: Contains DataFrames for LZc, LZsum, and gaps.
    """
    # Start MATLAB Engine
    try:
        eng = matlab.engine.start_matlab()
        print("Started MATLAB engine.")
    except Exception as e:
        print(f"Error starting MATLAB engine: {e}")
        return None

    # Add the path to the MATLAB functions directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    matlab_functions_path = os.path.join(current_dir, 'matlab_functions')
    if not os.path.exists(matlab_functions_path):
        print(f"MATLAB functions path does not exist: {matlab_functions_path}")
        eng.quit()
        return None
    eng.addpath(matlab_functions_path, nargout=0)
    print(f"Added MATLAB functions path: {matlab_functions_path}")

    # Call the MATLAB function to generate ogpath
    try:
        ogpath_matlab = eng.generate_ogpath(original_set_path, processed_set_path)
        print("Received ogpath from MATLAB.")
    except Exception as e:
        print(f"Error calling MATLAB function generate_ogpath: {e}")
        eng.quit()
        return None

    # Convert ogpath from MATLAB to Python list
    ogpath = np.array(ogpath_matlab).flatten()
    ogpath = ogpath.astype(int)

    # Stop MATLAB Engine
    eng.quit()
    print("Stopped MATLAB engine.")

    # Load processed epochs
    try:
        epochs = mne.read_epochs_eeglab(processed_set_path)
        data = epochs.get_data()  # Shape: (n_epochs, n_channels, n_times)
    except Exception as e:
        print(f"Error loading processed epochs: {e}")
        return None

    sz = data.shape  # (n_epochs, n_channels, n_times)

    # Define default channel groups
    default_channel_groups = {
        'fo_chans': [0, 1, 4, 5],       # Front-Occipital channels
        'ff_chans': [2, 3, 6],          # Front-Frontal channels
        'oo_chans': [7],                # Occipital-Occipital channel
        'glob_chans': list(range(8))    # Global channels (all channels)
    }

    # Use custom channel groups if provided; otherwise, use defaults
    if custom_channel_groups is not None:
        # Validate the custom_channel_groups structure
        if not isinstance(custom_channel_groups, dict):
            raise TypeError("custom_channel_groups must be a dictionary with group names as keys and lists of channel indices as values.")

        # Validate channel indices
        for group_name, channels in custom_channel_groups.items():
            if not isinstance(channels, list):
                raise TypeError(f"Channels for group '{group_name}' must be provided as a list of integers.")
            for ch in channels:
                if not isinstance(ch, int):
                    raise TypeError(f"Channel indices must be integers. Found {type(ch)} in group '{group_name}'.")
                if ch < 0 or ch >= sz[1]:
                    raise ValueError(f"Channel index {ch} in group '{group_name}' is out of bounds for the EEG data.")

        channel_groups = custom_channel_groups
    else:
        channel_groups = default_channel_groups

    fnames = list(channel_groups.keys())

    # Initialize dictionaries for LZ metrics
    lzc_values = {fname: [] for fname in fnames}
    lzsum_values = {fname: [] for fname in fnames}

    # Compute LZ metrics for each epoch and channel group
    for i in range(sz[0]):  # Epochs
        
        for ch in fnames:    # Channel groups
            chan_group = channel_groups[ch]

            # Extract data for the current channel group and epoch
            sample_data = data[i, chan_group, :]  # Shape: (n_channels_in_group, n_times)

            # Reshape data for LZc
            sample_data_lzc = sample_data.flatten()

            # Compute LZc
            
            dic_vec = LZ78(sample_data_lzc)

            # Normalization
            dis_data = np.random.permutation(sample_data_lzc)
            shuffled_lzc = LZ78(dis_data)
            if shuffled_lzc == 0:
                normalised_lz = np.nan
            else:
                normalised_lz = dic_vec / shuffled_lzc

            lzc_values[ch].append(normalised_lz)

            # Compute LZsum
            normalized_lz_sum = []
            for s in range(len(chan_group)):
                
                channel_data = sample_data[s, :]
                dic_val = LZ78(channel_data)
                shuffled_channel = np.random.permutation(channel_data)
                shuffled_val = LZ78(shuffled_channel)
                if shuffled_val == 0:
                    norm_lz = np.nan
                else:
                    norm_lz = dic_val / shuffled_val
                normalized_lz_sum.append(norm_lz)

            # Compute mean of LZsum
            norm_lzsum = np.nanmean(normalized_lz_sum)
            lzsum_values[ch].append(norm_lzsum)

    # Total number of original epochs
    try:
        original_epochs = mne.read_epochs_eeglab(original_set_path)
        no_epochs = len(original_epochs)
    except Exception as e:
        print(f"Error loading original epochs: {e}")
        return None

    # Validate ogpath length
    if len(ogpath) != sz[0]:
        print(f"Error: Length of ogpath ({len(ogpath)}) does not match number of processed epochs ({sz[0]}).")
        return None

    # Create DataFrames with 'epoch' column
    df_lzc = pd.DataFrame(lzc_values)
    df_lzc['epoch'] = ogpath
    df_lzsum = pd.DataFrame(lzsum_values)
    df_lzsum['epoch'] = ogpath

    # Reorder columns to have 'epoch' first
    df_lzc = df_lzc[['epoch'] + fnames]
    df_lzsum = df_lzsum[['epoch'] + fnames]

    # Sort DataFrames by 'epoch'
    df_lzc = df_lzc.sort_values('epoch').reset_index(drop=True)
    df_lzsum = df_lzsum.sort_values('epoch').reset_index(drop=True)

    # Collect missing epochs
    all_epochs = set(range(no_epochs))
    valid_epochs = set(ogpath)
    missing_epochs = sorted(all_epochs - valid_epochs)

    # Create a DataFrame for gaps
    df_gaps = pd.DataFrame({'gap_epoch': missing_epochs})

    # Optionally, save the DataFrames to files
    # df_lzc.to_excel('lz_c_results.xlsx', index=False)
    # df_lzsum.to_excel('lz_sum_results.xlsx', index=False)
    # df_gaps.to_excel('gaps.xlsx', index=False)

    print(f'Computed LZ metrics for epochs: {df_lzc["epoch"].tolist()}')
    print(f'Gaps found at epochs: {missing_epochs}')

    return {
        'lz_c': df_lzc,
        'lz_sum': df_lzsum,
        'gaps': df_gaps
    }