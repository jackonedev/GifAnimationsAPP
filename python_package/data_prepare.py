import pandas as pd
import pickle

def data_info(data, name="data"):
    """Funcion que devuelve informacion de un DataFrame en formato tipo DataFrame"""
    df = pd.DataFrame(pd.Series(data.columns))
    df.columns = ["columna"]
    df.columns.name = f"info de {name}"
    # df.index.name = 'index'
    df["Nan"] = data.isna().sum().values
    df["pct_nan"] = round(df["Nan"] / data.shape[0] * 100, 2)
    df["dtype"] = data.dtypes.values
    df["count"] = data.count().values
    df["pct_reg"] = ((data.notna().sum().values / data.shape[0]) * 100).round(2)
    df["count_unique"] = [
        len(data[elemento].value_counts()) for elemento in data.columns
    ]
    df = df.reset_index(drop=False)
    df = df.sort_values(by=["dtype", "count_unique"])
    df = df.reset_index(drop=True)
    return df


def save_object(objeto, file_name):
    """Guarda el objeto en un archivo pickle"""
    with open(file_name + ".pickle", "wb") as f:
        pickle.dump(objeto, f)



def check_type_dt(dataset):
    if isinstance(dataset.index, pd.core.indexes.datetimes.DatetimeIndex):
        print(f"\nSerie de tiempo: {dataset.index.name}\n")
        return dataset
    else:
        cols_dt = (dataset.dtypes == "<M8[ns]").values
        if cols_dt.sum() == 0:
            indice = check_type_str(dataset)
            print(f"\nSerie de tiempo: {indice}\n")
            dataset[indice] = pd.to_datetime(
                dataset[indice], infer_datetime_format=True
            )
            return dataset.set_index(indice)
        elif cols_dt.sum() == 1:
            indice = list(dataset.loc[:, cols_dt].columns)[0]
            print(f"\nSerie de tiempo: {indice}\n")
            return dataset.set_index(indice)
        else:
            indice = select_type_dt(dataset, cols_dt)
            print(f"\nSerie de tiempo: {indice}\n")
            return dataset.set_index(indice)


def check_type_str(dataset):
    cols_mask = (dataset.dtypes == "object").values
    cols_obj = dataset.loc[:, cols_mask].columns.values
    posible_dt = []
    if len(cols_obj) == 0:
        return print('No hay columnas tipo "object"')
    for i, elemento in enumerate(cols_obj):
        try:
            pd.to_datetime(dataset[elemento], infer_datetime_format=True)
            posible_dt.append(elemento)
        except:
            pass
    return select_type_dt(dataset, posible_dt)


def select_type_dt(dataset, posibles_dt):
    indice = list(dataset.loc[:, posibles_dt].columns)
    if len(indice) == 1:
        return indice[0]
    for i in range(len(indice)):
        indice[i] = str(i + 1) + ") {}".format(indice[i])
    print(">> SELECCION DE SERIE DE TIEMPO:")
    for i in range(len(indice)):
        print(indice[i])
    op = input(">> ")
    try:
        op = int(op) - 1  # para empezar a contar desde cero
        indice = list(dataset.loc[:, posibles_dt].columns)[op]
        return indice
    except:
        print("\nERROR: La opcion ingresada no corresponde\n")
        return
