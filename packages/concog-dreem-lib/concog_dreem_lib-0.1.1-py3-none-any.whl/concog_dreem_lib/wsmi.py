import numpy as np
import pandas as pd
import mne
from mne.utils import logger, _time_mask
from scipy.signal import butter, filtfilt
import matlab.engine
import os
import warnings
import math
from itertools import permutations

warnings.filterwarnings("ignore", category=RuntimeWarning)

def _get_weights_matrix(nsym):
    """Auxiliary function to create the weights matrix."""
    wts = np.ones((nsym, nsym))
    np.fill_diagonal(wts, 0)
    wts = np.fliplr(wts)
    np.fill_diagonal(wts, 0)
    wts = np.fliplr(wts)
    return wts



def _define_symbols(kernel):
    result_dict = dict()
    total_symbols = math.factorial(kernel)
    cursymbol = 0
    for perm in permutations(range(kernel)):
        order = ''.join(map(str, perm))
        if order not in result_dict:
            result_dict[order] = cursymbol
            cursymbol = cursymbol + 1
            result_dict[order[::-1]] = total_symbols - cursymbol
    result = []
    for v in range(total_symbols):
        for symbol, value in result_dict.items():
            if value == v:
                result += [symbol]
    return result

def _symb_python(data, kernel, tau):
    """Compute symbolic transform"""
    symbols = _define_symbols(kernel)
    dims = data.shape

    signal_sym_shape = list(dims)
    signal_sym_shape[1] = data.shape[1] - tau * (kernel - 1)
    signal_sym = np.zeros(signal_sym_shape, np.int32)

    count_shape = list(dims)
    count_shape[1] = len(symbols)
    count = np.zeros(count_shape, np.int32)

    for k in range(signal_sym_shape[1]):
        subsamples = range(k, k + kernel * tau, tau)
        ind = np.argsort(data[:, subsamples], 1)
        signal_sym[:, k, ] = np.apply_along_axis(
            lambda x: symbols.index(''.join(map(str, x))), 1, ind)

    count = np.double(np.apply_along_axis(
        lambda x: np.bincount(x, minlength=len(symbols)), 1, signal_sym))

    return signal_sym, (count / signal_sym_shape[1])

def _wsmi_python(data, count, wts):
    """Compute wsmi"""
    nchannels, nsamples, ntrials = data.shape
    nsymbols = count.shape[1]
    smi = np.zeros((nchannels, nchannels, ntrials), dtype=np.double)
    wsmi = np.zeros((nchannels, nchannels, ntrials), dtype=np.double)
    for trial in range(ntrials):
        for channel1 in range(nchannels):
            for channel2 in range(channel1 + 1, nchannels):
                pxy = np.zeros((nsymbols, nsymbols))
                for sample in range(nsamples):
                    pxy[data[channel1, sample, trial],
                        data[channel2, sample, trial]] += 1
                pxy = pxy / nsamples
                for sc1 in range(nsymbols):
                    for sc2 in range(nsymbols):
                        if pxy[sc1, sc2] > 0:
                            aux = pxy[sc1, sc2] * np.log(
                                pxy[sc1, sc2] /
                                count[channel1, sc1, trial] /
                                count[channel2, sc2, trial])
                            smi[channel1, channel2, trial] += aux
                            wsmi[channel1, channel2, trial] += \
                                (wts[sc1, sc2] * aux)
    wsmi = wsmi / np.log(nsymbols)
    smi = smi / np.log(nsymbols)
    return wsmi, smi

import numpy as np
import pandas as pd
import mne
from mne.utils import logger, _time_mask
from scipy.signal import butter, filtfilt
from scipy.special import factorial
import matlab.engine
import os
import warnings
import math
from itertools import permutations

warnings.filterwarnings("ignore", category=RuntimeWarning)

# (Keep all your auxiliary functions here, unchanged)

import numpy as np
import pandas as pd
import mne
from mne.utils import logger, _time_mask
from scipy.signal import butter, filtfilt
from scipy.special import factorial
import matlab.engine
import os
import warnings
import math
from itertools import permutations

warnings.filterwarnings("ignore", category=RuntimeWarning)

# (Keep all your auxiliary functions here, unchanged)

import numpy as np
import pandas as pd
import mne
from mne.utils import logger, _time_mask
from scipy.signal import butter, filtfilt
from scipy.special import factorial
import matlab.engine
import os
import warnings
import math
from itertools import permutations

warnings.filterwarnings("ignore", category=RuntimeWarning)

# Keep all your auxiliary functions here, unchanged
# _get_weights_matrix, _define_symbols, _symb_python, _wsmi_python

def epochs_compute_wsmi(epochs, kernel, tau, tmin=None, tmax=None,
                        backend='python', method_params=None, n_jobs='auto'):
    # Your original function remains unchanged
    if method_params is None:
        method_params = {}

    if n_jobs == 'auto':
        n_jobs = 1  # Simplify for now

    if 'bypass_csd' in method_params and method_params['bypass_csd']:
        logger.info('Bypassing CSD')
        csd_epochs = epochs
        picks = mne.pick_types(csd_epochs.info, meg=True, eeg=True)
    else:
        logger.info('Computing CSD')
        csd_epochs = mne.preprocessing.compute_current_source_density(
            epochs, lambda2=1e-5)
        picks = mne.io.pick.pick_types(csd_epochs.info, csd=True)

    freq = csd_epochs.info['sfreq']

    data = csd_epochs.get_data()[:, picks, ...]
    n_epochs = len(data)

    if 'filter_freq' in method_params:
        filter_freq = method_params['filter_freq']
    else:
        filter_freq = np.double(freq) / kernel / tau
    logger.info('Filtering at %.2f Hz' % filter_freq)
    b, a = butter(6, 2.0 * filter_freq / np.double(freq), 'lowpass')
    data = np.hstack(data)

    fdata = np.transpose(np.array(
        np.split(filtfilt(b, a, data), n_epochs, axis=1)), [1, 2, 0])

    time_mask = _time_mask(epochs.times, tmin, tmax)
    fdata = fdata[:, time_mask, :]
    logger.info("Performing symbolic transformation")
    sym, count = _symb_python(fdata, kernel, tau)
    nsym = count.shape[1]
    wts = _get_weights_matrix(nsym)
    logger.info("Running wsmi with python...")
    wsmi, smi = _wsmi_python(sym, count, wts)

    return wsmi, smi

def process_wsmi(original_set_path, processed_set_path, kernel, tau,
                 epoch_length, tmin=None, tmax=None, custom_channel_groups=None,
                 backend='python', method_params=None, n_jobs='auto'):
    """
    Processes an EEG '.set' file to compute wSMI metrics,
    maps them to their original epoch positions using MATLAB-generated ogpath,
    and returns the results as DataFrames.

    Parameters:
    - original_set_path (str): Path to the original '.set' EEG file.
    - processed_set_path (str): Path to the processed '.set' EEG file.
    - kernel (int): Number of samples to use to transform to a symbol.
    - tau (int): Number of samples left between the ones that define a symbol.
    - epoch_length (str): Description of epoch length (e.g., '4secs').
    - tmin (float, optional): Start time for time masking.
    - tmax (float, optional): End time for time masking.
    - custom_channel_groups (dict, optional): Custom channel groupings.
    - backend (str, optional): Backend to use ('python' or 'openmp').
    - method_params (dict, optional): Additional method parameters.
    - n_jobs (int or 'auto', optional): Number of jobs for parallel processing.

    Returns:
    - dict: Contains DataFrames for wSMI, SMI, and gaps.
    """

    print(f'Processing wSMI for {os.path.basename(processed_set_path)}')

    # Start MATLAB Engine
    try:
        eng = matlab.engine.start_matlab()
        print("Started MATLAB engine.")
    except Exception as e:
        print(f"Error starting MATLAB engine: {e}")
        return None  # Ensure a return value even on failure

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
        # Ensure that the 'method_params' is correctly used to bypass CSD
        # No need to set montage if bypassing CSD
    except Exception as e:
        print(f"Error loading processed epochs: {e}")
        return None

    # Compute wSMI
    wsmi, smi = epochs_compute_wsmi(
        epochs, kernel, tau, tmin, tmax, backend, method_params, n_jobs
    )

    # Total number of original epochs
    try:
        original_epochs = mne.read_epochs_eeglab(original_set_path)
        no_epochs = len(original_epochs)
    except Exception as e:
        print(f"Error loading original epochs: {e}")
        return None

    # Validate ogpath length
    if len(ogpath) != wsmi.shape[2]:
        print(f"Error: Length of ogpath ({len(ogpath)}) does not match number of processed epochs ({wsmi.shape[2]}).")
        return None

    # Collect missing epochs
    all_epochs = set(range(no_epochs))
    valid_epochs = set(ogpath)
    missing_epochs = sorted(all_epochs - valid_epochs)

    # Get channel names
    channel_names = epochs.ch_names
    n_channels = len(channel_names)

    # Prepare lists to collect results
    results = []

    # Iterate over processed epochs and map to original epochs
    for idx_processed, idx_original in enumerate(ogpath):
        if 0 <= idx_original < no_epochs:
            for ch1 in range(n_channels):
                for ch2 in range(ch1 + 1, n_channels):
                    result = {
                        'epoch': idx_original,
                        'channel_1': channel_names[ch1],
                        'channel_2': channel_names[ch2],
                        'wSMI': wsmi[ch1, ch2, idx_processed],
                        'SMI': smi[ch1, ch2, idx_processed]
                    }
                    results.append(result)
        else:
            print(f"Warning: Original epoch index {idx_original} out of bounds for processed epoch {idx_processed}.")

    # Create DataFrame from results
    df_wsmi = pd.DataFrame(results)

    # Sort the DataFrame by 'epoch'
    df_wsmi = df_wsmi.sort_values('epoch').reset_index(drop=True)

    # Create a DataFrame for gaps
    df_gaps = pd.DataFrame({'gap_epoch': missing_epochs})

    # Optionally, print information
    print(f'Computed wSMI metrics for epochs: {sorted(valid_epochs)}')
    print(f'Gaps found at epochs: {missing_epochs}')

    # Return the DataFrames
    return {
        'wsmi': df_wsmi,
        'gaps': df_gaps
    }