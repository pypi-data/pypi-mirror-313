import os
import numpy as np
import pandas as pd
import math
import mne
import matlab.engine
from itertools import permutations
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def compute_permutation_entropy(signal, m, tau):
    """
    Computes the normalized permutation entropy of a 1D signal.

    Parameters:
    - signal: 1D numpy array
    - m: Embedding dimension (kernel)
    - tau: Time delay (tau)

    Returns:
    - pe: Normalized permutation entropy value
    """
    n = len(signal)
    if n < m * tau:
        return np.nan  # Not enough data points

    possible_permutations = math.factorial(m)
    permutations_set = np.array(list(permutations(range(m))))
    c = np.zeros(len(permutations_set))

    # Build embedded vectors
    embedded_data = np.array([signal[i:i + m * tau:tau] for i in range(n - (m - 1) * tau)])
    # Map permutations to indices
    idx_dict = {tuple(perm): idx for idx, perm in enumerate(permutations_set)}
    # Sort embedded vectors and count permutations
    for vec in embedded_data:
        idx = tuple(np.argsort(vec))
        c[idx_dict[idx]] += 1

    # Normalize counts
    c = c / np.sum(c)
    # Compute permutation entropy
    pe = -np.nansum(c * np.log(c))
    # Normalize PE
    pe /= np.log(possible_permutations)
    return pe

def process_permutation_entropy(original_set_path, processed_set_path, epoch_length,
                                custom_channel_groups=None, kernel=3, tau=1):
    """
    Processes an EEG '.set' file to compute Permutation Entropy (PE) metrics,
    maps them to their original epoch positions using MATLAB-generated ogpath,
    and returns the results as DataFrames.

    Parameters:
    - original_set_path (str): Path to the original '.set' EEG file.
    - processed_set_path (str): Path to the processed '.set' EEG file.
    - epoch_length (str): Description of epoch length (e.g., '4secs').
    - custom_channel_groups (dict, optional): Custom channel groupings.
    - kernel (int): The number of samples to use to transform to a symbol.
    - tau (int): The number of samples left between the ones that define a symbol.

    Returns:
    - dict: Contains DataFrames for PE and gaps.
    """

    print(f'Processing permutation entropy for {os.path.basename(processed_set_path)}')

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

    # Convert ogpath from MATLAB to Python array
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

    # Initialize list to collect results
    results = []

    # Collect epoch indices
    epoch_indices = []

    # Compute PE metrics for each epoch and channel group
    for idx_processed in range(sz[0]):  # Epochs
        idx_original = ogpath[idx_processed]
        epoch_indices.append(idx_original)

        for ch in fnames:    # Channel groups
            chan_group = channel_groups[ch]

            # Extract data for the current channel group and epoch
            sample_data = data[idx_processed, chan_group, :]  # Shape: (n_channels_in_group, n_times)

            # Flatten the data across channels
            sample_data_flat = sample_data.flatten()

            # Compute PE
            try:
                pe_value = compute_permutation_entropy(sample_data_flat, kernel, tau)
            except Exception as e:
                print(f"Error computing PE for epoch {idx_original}, group {ch}: {e}")
                pe_value = np.nan

            # Save the result
            results.append({
                'epoch': idx_original,
                'channel_group': ch,
                'PE': pe_value
            })

    # Total number of original epochs
    try:
        original_epochs = mne.read_epochs_eeglab(original_set_path)
        no_epochs = len(original_epochs)
    except Exception as e:
        print(f"Error loading original epochs: {e}")
        return None

    # Collect missing epochs
    all_epochs = set(range(no_epochs))
    valid_epochs = set(epoch_indices)
    missing_epochs = sorted(all_epochs - valid_epochs)

    # Create DataFrame from results
    df_pe = pd.DataFrame(results)

    # Sort the DataFrame by 'epoch'
    df_pe = df_pe.sort_values('epoch').reset_index(drop=True)

    # Create a DataFrame for gaps
    df_gaps = pd.DataFrame({'gap_epoch': missing_epochs})

    # Optionally, print information
    print(f'Computed Permutation Entropy for epochs: {sorted(valid_epochs)}')
    print(f'Gaps found at epochs: {missing_epochs}')

    return {
        'pe': df_pe,
        'gaps': df_gaps
    }