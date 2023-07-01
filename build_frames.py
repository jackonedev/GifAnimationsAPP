import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
import datetime as dt
from rich import print

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
    repeat=True##TODO: El parámetro repeat está en plot_data(), la cosa es que por ahora puedo diferenciar entre dos estilos diferentes de construir el deque
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
            dy = deque(np.zeros(window)*data[label].iloc[0], maxlen=window)
        drop_elements = list(data[label].values)[-1::-1]
    #
    lista_frames = create_frame(drop_elements, dy)
    row_keys = [f'{i}' for i in range(window)]
    return pd.DataFrame(lista_frames, columns=row_keys)



def main():
    data = pd.read_pickle('data/data-processed.pkl')
    sample = data["MLN-EE-76-U-2_CAS-P.PV"].to_frame()
    dates = build_frames(data.reset_index(), data.reset_index().columns[0])
    dates = dates.replace(0, pd.Timestamp('00:00:00').floor('s')).applymap(lambda x: x.to_pydatetime().strftime('%M:%S'))
    frames = build_frames(sample, sample.columns[0])


    print(frames)

if __name__ ==  '__main__' :
    main()
