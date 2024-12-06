# LUMO Damage Detection Evaluation Package

This package provides a standardized framework for evaluating damage detection and localization strategies using the LUMO dataset. Users can input timestamps alongside their corresponding anomaly indices, and the package computes various performance scores for each damage case, promoting consistency in damage detection evaluation.

## Features

- **Standardized Evaluation Metrics**: Calculates TPR and FPR at a threshold set such as FPR for training data is 1%.
The training dataset should be only the first moth of data
- **Damage Case Analysis**: Provides detailed performance evaluations for each specific damage scenario within the LUMO dataset.


## Installation

To install the package, run:

```bash
pip install evaluation_lumo

## Usage

To use the package, import the `evaluation_lumo.evaluation` module and call the `compute_tr_by_events` function or `compute_mean_variation` function.

```python
from evaluation_lumo.evaluation import compute_tr_by_events, compute_mean_variation

# Example usage

date_index = pd.date_range(start='2021-08-01', ends="2022-08-01", freq='10T')
associated_damage_index = np.random.random(len(date_index))
compute_tr_by_events(date_index, associated_damage_index)
compute_mean_variation(date_index, associated_damage_index)
```
