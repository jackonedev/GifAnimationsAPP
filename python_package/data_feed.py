import pandas as pd
from collections import deque
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

plt.ion()


def clean_labels(data_labels):
    cleaned_labels = []
    for label in data_labels:
        # Remove the first occurrence of "[" and "]"
        if "[" in label:
            label = label.replace("[", "", 1)
        if "]" in label:
            label = label.replace("]", "", 1)
        
        # Replace spaces with underscores
        if " " in label:
            label = label.replace(" ", "_")
        
        cleaned_labels.append(label)
    
    return cleaned_labels


def build_frames(data: pd.DataFrame, label: str, window:int=0) -> pd.DataFrame:
    """Storage all the results of processing the deque object"""
    if not window:
        window = len(data)
    drop_elements = list(data[label].values)[-2::-1]
    dy = deque(data[label].values, maxlen=len(data))
    lista_frames = [dy.copy()]

    while len(drop_elements) > 0:
        dy.append(drop_elements.pop())
        lista_frames.append(dy.copy())

    row_keys = [f'{i}' for i in data.index]

    df = pd.DataFrame(lista_frames, columns=row_keys)

    return df.iloc[:,:window]


def plot_data(df, speed=100, repeat=True):
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    
    def update(i):
        ax.clear()
        line, = ax.plot(df.iloc[i])
        return line, 

    return FuncAnimation(fig, update, frames=len(df), interval=speed, blit=True, repeat=repeat)