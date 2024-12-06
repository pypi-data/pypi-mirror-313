from __future__ import annotations

import pandas as pd


def label_events(timestamps, events):
    """
    Label each timestamp based on defined events.

    Parameters:
    - timestamps (pd.Series): Series of datetime timestamps.
    - events (dict): Dictionary of event definitions with 'start' and 'end' times.

    Returns:
    - pd.Series: Series of labels corresponding to each timestamp.
    """
    # Initialize labels with the same index as timestamps and with no event
    labels = pd.Series(index=timestamps, dtype=object)
    labels = labels.fillna("no_event")
    # Assign labels based on events
    for event_name, event_info in events.items():
        start = pd.to_datetime(event_info["start"])
        end = pd.to_datetime(event_info["end"])
        mask = (timestamps >= start) & (timestamps <= end)
        labels.loc[mask] = event_name
    return labels
