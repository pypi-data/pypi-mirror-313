% File: matlab_functions/generate_ogpath.m

function ogpath = generate_ogpath(original_set_path, processed_set_path)
    % Generates ogpath mapping from processed epochs to original epochs
    % using the urevent field in EEGLAB datasets.
    %
    % Inputs:
    %   original_set_path  - Path to the original .set EEG file
    %   processed_set_path - Path to the processed .set EEG file
    %
    % Output:
    %   ogpath - Array mapping processed epochs to original epochs (zero-based indexing)

    % -----------------------------
    % Load Original Dataset
    % -----------------------------
    fprintf('Loading original dataset...\n');
    EEG_original = pop_loadset('filename', original_set_path);
    if isempty(EEG_original)
        error('Failed to load the original dataset.');
    end

    % -----------------------------
    % Load Processed Dataset
    % -----------------------------
    fprintf('Loading processed dataset...\n');
    EEG_processed = pop_loadset('filename', processed_set_path);
    if isempty(EEG_processed)
        error('Failed to load the processed dataset.');
    end

    % -----------------------------
    % Generate ogpath Using urevent Field
    % -----------------------------
    fprintf('Generating ogpath mapping using urevent field...\n');

    % Create a mapping from urevent to original epoch index
    urevent_to_epoch = containers.Map('KeyType', 'double', 'ValueType', 'double');
    for i = 1:length(EEG_original.event)
        urevent = EEG_original.event(i).urevent;
        if ~isKey(urevent_to_epoch, urevent)
            epoch_num = EEG_original.event(i).epoch;
            urevent_to_epoch(urevent) = epoch_num;
        end
    end

    % Initialize ogpath
    ogpath = NaN(1, EEG_processed.trials);

    % Map processed epochs to original epochs using urevent
    for i = 1:EEG_processed.trials
        % Get event indices and latencies in this epoch
        event_indices = EEG_processed.epoch(i).event;
        event_latencies = EEG_processed.epoch(i).eventlatency;
        if iscell(event_latencies)
            event_latencies = cell2mat(event_latencies);
        end
        % Find the time-locking event (latency zero)
        idx_zero_latency = find(event_latencies == 0);
        if ~isempty(idx_zero_latency)
            event_idx = event_indices(idx_zero_latency(1));
            urevent = EEG_processed.event(event_idx).urevent;
            if isKey(urevent_to_epoch, urevent)
                original_epoch_num = urevent_to_epoch(urevent);
                ogpath(i) = original_epoch_num - 1;  % Zero-based indexing
            else
                fprintf('Warning: urevent %d not found in original dataset for processed epoch %d.\n', urevent, i);
                ogpath(i) = NaN;
            end
        else
            fprintf('Warning: No time-locking event found in processed epoch %d.\n', i);
            ogpath(i) = NaN;
        end
    end

    % -----------------------------
    % Verify ogpath
    % -----------------------------
    fprintf('Verifying ogpath...\n');
    fprintf('Total original epochs: %d\n', EEG_original.trials);
    fprintf('Total processed epochs: %d\n', EEG_processed.trials);
    fprintf('ogpath length: %d\n', length(ogpath));

    % Check for duplicates in ogpath
    if length(unique(ogpath(~isnan(ogpath)))) ~= length(ogpath(~isnan(ogpath)))
        warning('Duplicate values found in ogpath.');
    else
        fprintf('No duplicates found in ogpath.\n');
    end

    % Print the first 10 values of ogpath
    num_to_display = min(10, length(ogpath));
    fprintf('First %d values of ogpath:\n', num_to_display);
    disp(ogpath(1:num_to_display));
end