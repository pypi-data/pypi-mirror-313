
# concog_dreem_lib

A Python library for EEG data analysis, including Lempel-Ziv (LZ) complexity, weighted Symbolic Mutual Information (wSMI), Power Spectral Density (PSD) analysis, and Permutation Entropy calculations. This library is designed to work with EEG data and integrates MATLAB functions via the MATLAB Engine API for Python.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Dependencies](#dependencies)
  - [MATLAB and MATLAB Engine API](#matlab-and-matlab-engine-api)
- [Usage](#usage)
  - [LZ Complexity](#lz-complexity)
  - [Weighted Symbolic Mutual Information (wSMI)](#weighted-symbolic-mutual-information-wsmi)
  - [Power Spectral Density (PSD) Analysis](#power-spectral-density-psd-analysis)
  - [Permutation Entropy](#permutation-entropy)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **LZ Complexity**: Compute the Lempel-Ziv complexity of EEG signals.
- **wSMI Calculations**: Compute weighted Symbolic Mutual Information from EEG data.
- **PSD Analysis**: Perform Power Spectral Density analysis with options for FOOOF fitting.
- **Permutation Entropy**: Calculate permutation entropy measures for time-series data.

## Installation

Install the package using pip:

```bash
pip install concog_dreem_lib