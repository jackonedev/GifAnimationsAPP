import numpy as np
import pandas as pd
from collections import deque
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

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
    repeat=True##TODO: testear la funcion window: window=len(data)
    if not window:
        window = len(data)
        repeat = False
    #
    if repeat:
        drop_elements = list(data[label].values)[-2::-1]
        dy = deque(data[label].values, maxlen=len(data))
    else:
        if isinstance(data[label].iloc[0], pd._libs.tslibs.timestamps.Timestamp):
            print ('Según  ISO 8601: formato estandar para representar fechas y tiempos')
            dy = deque(np.zeros(window), maxlen=window)
        else:
            dy = deque(np.zeros(window), maxlen=window)
        drop_elements = list(data[label].values)[-1::-1]
    #
    lista_frames = create_frame(drop_elements, dy)
    row_keys = [f'{i}' for i in range(window)]
    return pd.DataFrame(lista_frames, columns=row_keys)



def plot_data(data, label, title, unit, grid_y=3, fps=24, repeat=True, cache=False):

    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    interval = 1000/fps
    
    index_label =  data.reset_index().columns[0]
    dx = build_frames(data.reset_index(), index_label)
    ## La siguiente línea de código tarda 22seg en ejecutarse
    dx = dx.replace(0, pd.Timestamp('00:00:00').floor('s')).applymap(lambda x: x.to_pydatetime().strftime('%M:%S'))
    df = build_frames(data,label)


    def update(i):
        date = dx.iloc[i]
        frame = df.iloc[i]
        index_min = int(date[frame !=0].index[0])
        eje_x = date.loc[:str(int(index_min)-1)].index.to_list() + date.iloc[int(index_min):].to_list()
        frame.index = eje_x

        ax.clear()
        line, = ax.plot(frame)
        ax.set_ylim(y_lim_min, y_lim_max)
        ax.set_yticks(np.linspace(y_lim_min, y_lim_max, grid_y))

        if i < 180:
            ax.set_xticks(eje_x[-1])
        elif i < 600:
            lista_eje_x = []
            lista_eje_x.append(eje_x[-181])
            lista_eje_x.append(eje_x[-1])
            ax.set_xticks(lista_eje_x)
        else:
            lista_eje_x = []
            lista_eje_x.append(eje_x[-181])
            lista_eje_x.append(eje_x[-1])
            lista_eje_x.append(eje_x[-i-1])
            lista_eje_x.append(eje_x[-len(eje_x[-i-1:-180])//2-180])
            ax.set_xticks(lista_eje_x)
        
        #TODO: esta variable global no se actualiza#TODO: esta variable se obitene dentro de esta funcion
        
        # plt.title(title)
        # plt.xlabel('Time')
        # plt.ylabel(unit)
        # plt.tight_layout()


        # ax.set_title('Hola mundo!')
        # ax.set_xlabel('Tiempo')
        # ax.set_ylabel('Valor')
        # ax.set_xlim(0, len(df.columns) - 1)
        # ax.set_xticks(range(0, len(df.columns), 5))
        # ax.set_xticklabels([str(x) for x in range(0, len(df.columns), 5)])
        
        return line, 


    return FuncAnimation(fig, update, frames=len(df), interval=interval, blit=True, repeat=repeat, cache_frame_data=cache)


### borrar este
def plot_data_original(df, dates, lapse, fps=24, repeat=True, cache=False):
    pass
#     fig, ax = plt.subplots()
#     line, = ax.plot([], [])
#     interval = 1000/fps
    
#     dates = data.index
#     dates = mdates.drange(dates[0], dates[-1], dt.timedelta(seconds=1))

#     def update(i):
#         ax.clear()
#         ax.set_xlim(dx[0], dx[-1])
#         ax.set_xticks(np.linspace(dates[0], dates[-1], 10))

#         ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(mdates.SecondLocator()))

#         # ax.set_title('Hola mundo!')
#         # ax.set_xlabel('Tiempo')
#         # ax.set_ylabel('Valor')
#         # ax.set_xlim(0, len(df.columns) - 1)
#         ax.set_ylim(y_lim_min, y_lim_max)#TODO: esta variable global no se actualiza
#         # ax.set_xticks(range(0, len(df.columns), 5))
#         # ax.set_xticklabels([str(x) for x in range(0, len(df.columns), 5)])
#         line, = ax.plot(df.iloc[i])
#         return line, 

#     return FuncAnimation(fig, update, frames=len(df), interval=interval, blit=True, repeat=repeat, cache_frame_data=cache)



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



def apply_dark_mode():
    """https://matplotlib.org/3.5.0/tutorials/introductory/customizing.html
    https://matplotlib.org/3.1.1/tutorials/colors/colors.html"""

    import matplotlib.pyplot as plt
    from matplotlib import cycler

    # import matplotlib as mpl

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

    plt.rc("grid", color="474A4A", linestyle="--", alpha=0.7)
    plt.rc("xtick", color="0.81", labelsize=12)
    plt.rc("ytick", direction="out", color="0.81", labelsize=12)
    plt.rc("legend", facecolor="#313233", edgecolor="#313233")
    plt.rc("text", color="#C9C9C9")

    plt.rcParams["axes.grid.which"] = "major" 
    plt.rcParams["axes.grid.axis"] = "y"










if __name__ == "__main__":
    main()
