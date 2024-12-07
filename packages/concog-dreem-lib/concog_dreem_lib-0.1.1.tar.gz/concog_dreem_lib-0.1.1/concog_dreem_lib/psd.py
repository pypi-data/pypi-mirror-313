import numpy as np
import pandas as pd
import mne
import matlab.engine
import os
import warnings
from mne.time_frequency import psd_array_welch
from fooof import FOOOF
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=RuntimeWarning)

def process_psd(original_set_path, processed_set_path, epoch_length,
                normalize_total_power=True, band_power_method='psd_integration',
                plot_fooof=False, plot_epochs=None, plot_channel=None):
    """
    Processes an EEG '.set' file to compute the offset, exponent, and band powers from power spectral analysis,
    for each epoch and channel, maps them to their original epoch positions
    using MATLAB-generated ogpath, and returns the results as DataFrames.

    Parameters:
    - original_set_path (str): Path to the original '.set' EEG file.
    - processed_set_path (str): Path to the processed '.set' EEG file.
    - epoch_length (str): Description of epoch length (e.g., '4secs').
    - normalize_total_power (bool, optional): If True, normalizes band power by total power over the spectrum.
    - band_power_method (str, optional): Method to calculate band power. Options are 'psd_integration' and 'fooof_peaks'.
    - plot_fooof (bool, optional): If True, generates plots of the FOOOF fit.
    - plot_epochs (list, optional): List of epoch indices to plot. If None, plots no epochs.
    - plot_channel (str, optional): Name of the channel to plot. If None, plots all channels.

    Returns:
    - dict: Contains DataFrames for computed measures and gaps.
    """
    # Extract file name without extension
    file_name = os.path.splitext(os.path.basename(processed_set_path))[0]
    print(f'Processing PSD for {file_name}')

    # Start MATLAB Engine
    try:
        eng = matlab.engine.start_matlab()
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
    except Exception as e:
        print(f"Error calling MATLAB function generate_ogpath: {e}")
        eng.quit()
        return None

    # Convert ogpath from MATLAB to Python array
    ogpath = np.array(ogpath_matlab).flatten().astype(int)

    # Stop MATLAB Engine
    eng.quit()

    # Load processed epochs
    try:
        epochs = mne.read_epochs_eeglab(processed_set_path)
        data = epochs.get_data()  # Shape: (n_epochs, n_channels, n_times)
        sfreq = epochs.info['sfreq']
    except Exception as e:
        print(f"Error loading processed epochs: {e}")
        return None

    n_epochs, n_channels, n_times = data.shape
    # Initialize lists for measures
    results = []

    # Define frequency bands
    freq_bands = {
        'Delta': [1, 4],
        'Theta': [4, 8],
        'Alpha': [8, 13],
        'Beta': [13, 30],
        'Gamma': [30, 45]
    }

    # Parameters for PSD and FOOOF
    window_length = int(sfreq * 2)  # 2-second windows
    n_per_seg = min(window_length, n_times)
    n_fft = n_per_seg
    n_overlap = n_per_seg // 2
    freq_range = [1, 45]  # Frequency range for fitting

    # Handle plotting options
    if plot_epochs is None:
        plot_epochs = []

    # Create directory for plots
    if plot_fooof and plot_epochs:
        plots_dir = os.path.join(os.getcwd(), 'fooof_plots')
        os.makedirs(plots_dir, exist_ok=True)

    # Iterate over epochs
    for idx_processed in range(n_epochs):
        idx_original = ogpath[idx_processed]
        # Check if we should plot this epoch
        plot_this_epoch = plot_fooof and (idx_original in plot_epochs)
        # For plotting, if plot_channel is specified, get its index
        if plot_channel is not None and plot_channel in epochs.ch_names:
            plot_ch_idx = epochs.ch_names.index(plot_channel)
        else:
            plot_ch_idx = None  # Plot all channels

        # Iterate over channels
        for ch_idx in range(n_channels):
            channel_name = epochs.ch_names[ch_idx]
            epoch_data = data[idx_processed, ch_idx, :] * 1e6  # Convert to microvolts

            # Compute PSD
            psd, freqs = psd_array_welch(
                epoch_data,
                sfreq=sfreq,
                fmin=1,
                fmax=45,
                n_fft=n_fft,
                n_overlap=n_overlap,
                n_per_seg=n_per_seg,
                average='mean'
            )

            psd += 1e-12  # Avoid log(0) issues

            # Fit FOOOF
            fm = FOOOF(peak_width_limits=[2, 12], verbose=False)
            fm.fit(freqs, psd, freq_range)

            # Extract offset and exponent
            aperiodic_params = fm.aperiodic_params_
            if len(aperiodic_params) >= 2:
                offset = aperiodic_params[0]
                exponent = aperiodic_params[1]
            else:
                offset = np.nan
                exponent = np.nan

            # Initialize band power dict for this epoch and channel
            band_powers = {}
            # Depending on the method, compute band powers
            if band_power_method == 'psd_integration':
                total_power = np.trapz(psd, freqs)
                # Compute band powers by integrating PSD over bands
                for band_name, band_range in freq_bands.items():
                    band_indices = np.where((freqs >= band_range[0]) & (freqs <= band_range[1]))[0]
                    if band_indices.size > 1:
                        band_psd = psd[band_indices]
                        band_freqs = freqs[band_indices]
                        band_power = np.trapz(band_psd, band_freqs)
                        if normalize_total_power:
                            if total_power > 0:
                                band_power = band_power / total_power  # Result is fraction between 0 and 1
                            else:
                                band_power = np.nan
                    else:
                        band_power = np.nan
                    band_powers[band_name] = band_power

            elif band_power_method == 'fooof_peaks':
                # Extract peaks from FOOOF
                peak_params = fm.get_params('peak_params')
                # peak_params is an array of [CF, PW, BW]
                # Sum the peak powers for peaks within each band
                if peak_params.size > 0:
                    total_peak_power = np.sum(peak_params[:, 1])
                else:
                    total_peak_power = np.nan
                for band_name, band_range in freq_bands.items():
                    # Find peaks within band
                    band_peaks = peak_params[
                        (peak_params[:, 0] >= band_range[0]) & (peak_params[:, 0] <= band_range[1])
                    ]
                    # Sum the peak powers (in log power)
                    if band_peaks.size > 0:
                        band_power = np.sum(band_peaks[:, 1])
                    else:
                        band_power = np.nan
                    # Optionally normalize band powers
                    if normalize_total_power and total_peak_power > 0:
                        band_power = band_power / total_peak_power
                    band_powers[band_name] = band_power

            else:
                print(f"Unknown band_power_method: {band_power_method}")
                return None

            # Append results
            result = {
                'epoch': idx_original,
                'channel': channel_name,
                'Offset': offset,
                'Exponent': exponent,
            }
            # Add band powers to result
            for band_name in freq_bands:
                result[f'{band_name}_Power'] = band_powers.get(band_name, np.nan)
            # Append to results list
            results.append(result)

            # Plot FOOOF fit if enabled and conditions are met
            if plot_this_epoch and (plot_ch_idx is None or ch_idx == plot_ch_idx):
                plt.figure(figsize=(10, 6))
                fm.plot(plot_peaks='shade', add_legend=True)
                plt.title(f"FOOOF Fit - Epoch {idx_original} - Channel {channel_name}")
                plot_filename = f"fooof_fit_epoch_{idx_original}_channel_{channel_name}.png"
                plot_path = os.path.join(plots_dir, plot_filename)
                plt.savefig(plot_path)
                plt.close()
                print(f"Saved FOOOF plot to {plot_path}")

    # Create DataFrame from results
    measures_df = pd.DataFrame(results)

    # Total number of original epochs
    try:
        original_epochs = mne.read_epochs_eeglab(original_set_path)
        no_epochs = len(original_epochs)
    except Exception as e:
        print(f"Error loading original epochs: {e}")
        return None

    # Collect missing epochs
    all_epochs = set(range(no_epochs))
    valid_epochs = set(ogpath)
    missing_epochs = sorted(all_epochs - valid_epochs)

    # Create DataFrame for gaps
    df_gaps = pd.DataFrame({'gap_epoch': missing_epochs})

    # Optionally, print information
    print(f'Computed PSD measures for epochs: {sorted(valid_epochs)}')
    print(f'Gaps found at epochs: {missing_epochs}')

    return {
        'measures': measures_df,
        'gaps': df_gaps
    }