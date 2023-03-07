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


def build_frames(data: pd.DataFrame, label: str, window:int=0) -> pd.DataFrame:# (2): agregar el parametro repear para ver que forma va a tener el deque
    """Storage all the results of processing the deque object"""
    if not window:
        window = len(data)
    drop_elements = list(data[label].values)[-2::-1]
    dy = deque(data[label].values, maxlen=len(data))#(1) ORIGINALMENTE ERA np.zeros(window)
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


def apply_dark_mode():
    """https://matplotlib.org/3.5.0/tutorials/introductory/customizing.html
    https://matplotlib.org/3.1.1/tutorials/colors/colors.html"""

    import matplotlib.pyplot as plt

    import matplotlib as mpl
    from matplotlib import cycler

    colors = cycler(
        "color", ["#669FEE", "#66EE91", "#9988DD", "#EECC55", "#88BB44", "#FFBBBB"]
    )

    plt.rc("figure", facecolor="#313233")
    plt.rc(
        "axes",
        facecolor="#313233",
        edgecolor="none",
        axisbelow=True,
        grid=True,
        prop_cycle=colors,
        labelcolor="0.81",
    )
    plt.rc("grid", color="474A4A", linestyle="solid")
    plt.rc("xtick", color="0.81", labelsize=12)
    plt.rc("ytick", direction="out", color="0.81", labelsize=12)
    plt.rc("legend", facecolor="#313233", edgecolor="#313233")
    plt.rc("text", color="#C9C9C9")    