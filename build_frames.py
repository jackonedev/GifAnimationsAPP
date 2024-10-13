"""
Module for data preprocessing for real-time time-series visualization.

This module provides functions to create frames for animation plots from time-series data.
"""

from collections import deque

import numpy as np
import pandas as pd


def create_frames(
    data_points: list,
    data_buffer: deque,
) -> list:
    """
    Create a list of frames by appending data points to a deque buffer.

    Args:
    - data_points (list): List of data points to append to the buffer.
    - data_buffer (deque): Deque buffer to store the data points.

    Returns:
    - list: List of frames, where each frame is a copy of the deque buffer.
    """
    frames = []
    while len(data_points) > 0:
        # Append the last data point to the buffer and remove it from the list
        data_buffer.append(data_points.pop())
        # Create a copy of the buffer and add it to the list of frames
        frames.append(data_buffer.copy())
    return frames


def build_animation_frames(
    data: pd.DataFrame,
    column_name: str,
    window_size: int = 0,
) -> pd.DataFrame:
    """
    Create a DataFrame of frames for animation plots from time-series data.

    Args:
    - data (pd.DataFrame): Time-series data with a single column.
    - column_name (str): Name of the column in the DataFrame.
    - window_size (int, optional): Size of the window for the animation. Defaults to 0.

    Returns:
    - pd.DataFrame: DataFrame where each row represents a single frame of the animation plot.

    Notes:
    - If window_size is 0, the window size will be set to the length of the data.
    - The function also sets global variables y_lim_max and y_lim_min for axis formatting.
    """
    global y_lim_max, y_lim_min
    # Set global variables for axis formatting
    y_lim_max = data[column_name].max()
    y_lim_min = data[column_name].min()

    repeat = True
    if not window_size:
        window_size = len(data)
        repeat = False

    if repeat:
        # Get the data points in reverse order, excluding the last point
        data_points = list(data[column_name].values)[-2::-1]
        # Create a deque buffer with the data points
        data_buffer = deque(data[column_name].values, maxlen=len(data))
    else:
        # Check if the first value is a timestamp
        if isinstance(data[column_name].iloc[0], pd._libs.tslibs.timestamps.Timestamp):
            # Create a deque buffer with zeros
            data_buffer = deque(np.zeros(window_size), maxlen=window_size)
        else:
            # Create a deque buffer with zeros scaled by the first value
            data_buffer = deque(
                np.zeros(window_size) * data[column_name].iloc[0], maxlen=window_size
            )
        # Get the data points in reverse order
        data_points = list(data[column_name].values)[-1::-1]

    # Create the list of frames and the row keys for the DataFrame
    frames = create_frames(data_points, data_buffer)
    row_keys = [f"{i}" for i in range(window_size)]

    return pd.DataFrame(frames, columns=row_keys)


def main():
    data = pd.read_pickle('data/data-processed.pkl')
    sample = data["MLN-EE-76-U-2_CAS-P.PV"].to_frame()
    dates = build_animation_frames(data.reset_index(), data.reset_index().columns[0])
    dates = dates.replace(0, pd.Timestamp('00:00:00').floor('s')).applymap(lambda x: x.to_pydatetime().strftime('%M:%S'))
    frames = build_animation_frames(sample, sample.columns[0])


    print(frames)

if __name__ ==  '__main__' :
    main()
