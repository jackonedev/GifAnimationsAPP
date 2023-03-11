import numpy as np
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


def create_frame(drop_elements:list, dy:deque,) -> pd.DataFrame:#TODO: cambiar el nombre de los parámetros
    lista_frames = []
    while len(drop_elements) > 0:
        dy.append(drop_elements.pop())
        lista_frames.append(dy.copy())
    return lista_frames

def build_frames(data: pd.DataFrame, label: str, window:int=0) -> pd.DataFrame:

    """Storage all the results of processing the deque object
    Also, create global variables por axis formating
    """

    global y_lim_max, y_lim_min
    y_lim_max = data[label].max()
    y_lim_min = data[label].min()
    repeat=True
    if not window:
        window = len(data)
        repeat = False
    #
    if repeat:
        drop_elements = list(data[label].values)[-2::-1]
        dy = deque(data[label].values, maxlen=len(data))
    else:
        dy = deque(np.zeros(window)*data[label].iloc[0], maxlen=window)
        drop_elements = list(data[label].values)[-1::-1]
    #
    lista_frames = create_frame(drop_elements, dy)
    row_keys = [f'{i}' for i in range(window)]
    return pd.DataFrame(lista_frames, columns=row_keys)



def plot_data(df, fps=24, repeat=True, cache=False):
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    interval = 1000/fps
    ax.set_xlim(0, 5)
    
    
    # def update(i):
    #     ax.clear()
    #     line, = ax.plot(df.iloc[i])#, c='steelblue', linewidth=2.5,markeredgecolor='black', markeredgewidth=1.2, label='y = x^2')
        

    #     return line, 


    def update(i):
        ax.clear()
        ax.set_title('Hola mundo!')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Valor')
        ax.set_xlim(0, len(df.columns) - 1)
        ax.set_ylim(y_lim_min, y_lim_max)
        ax.set_xticks(range(0, len(df.columns), 5))
        ax.set_xticklabels([str(x) for x in range(0, len(df.columns), 5)])
        line, = ax.plot(df.iloc[i])
        return line, 

    return FuncAnimation(fig, update, frames=len(df), interval=interval, blit=True, repeat=repeat, cache_frame_data=cache)


def main():
    file_name = "data-processed.pkl"
    try:
        path = "01-data-animation/app/data/"
        data = pd.read_pickle(path + file_name)
    except:
        path = "../data/"
        data = pd.read_pickle(path + file_name)


    # print (data.head()) # <--  primera ejecucion
    selected_vars = ["MLN-EE-76-U-2_CAS-P.PV", "TFS-EE-176-MB_FC-HDR-DEN-OBS.PV"]

    label = {'pressure': selected_vars[0], 'flow_rate': selected_vars[1]}
    units = {'pressure': 'PSIg', 'flow_rate': 'm3/h'}

    frames = {}
    frames['pressure'] = build_frames(data, label['pressure'])
    frames['flow_rate'] = build_frames(data, label['flow_rate'], window=80)
#    print (frames['flow_rate'].tail()) # <--  segunda ejecucion
#    print (len(frames['flow_rate']))

    ani = plot_data(frames['flow_rate'])

if __name__ == "__main__":
    main()
