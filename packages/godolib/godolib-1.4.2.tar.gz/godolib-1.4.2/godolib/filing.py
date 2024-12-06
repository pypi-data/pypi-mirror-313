import os
import chardet
import pandas as pd
import numpy as np
from datetime import datetime
import json

def general_nested_dict_to_dataframe(nested_dict, parent_keys=None):
    """
    Converts a nested dictionary into a flat pandas DataFrame.

    Each row of the DataFrame represents a unique path from the root to a leaf value in the dictionary.
    The path is split across hierarchical columns, and the values are stored in a separate column.

    Parameters:
    - nested_dict (dict): A dictionary with potentially multiple levels of nesting. 
                          The keys at each level represent hierarchical labels, 
                          and the leaf nodes contain the values to be extracted.
    - parent_keys (list, optional): A list of keys representing the current path in the recursion. 
                                     This is primarily used internally during recursion. Defaults to an empty list.

    Returns:
    - pd.DataFrame: A DataFrame where:
                     - Each row corresponds to a unique path from the root of the dictionary to a leaf value.
                     - The columns `Level_0, Level_1, ..., Level_n` represent the hierarchical keys.
                     - The final column, `Value`, contains the associated values.

    Example:
    nested_dict = {
        "Category A": {
            "Subcategory A1": {
                "Item 1": 10,
                "Item 2": 20,
            },
            "Subcategory A2": {
                "Item 3": 30
            }
        },
        "Category B": {
            "Subcategory B1": {
                "Item 4": 40
            }
        }
    }

    df = general_nested_dict_to_dataframe(nested_dict)
    print(df)
    """
    
    if parent_keys is None:
        parent_keys = []

    rows = []

    def flatten(current_dict, keys):
        """
        Recursively flattens the nested dictionary and appends the path and value to the `rows` list.

        Parameters:
        - current_dict (dict): The current level of the nested dictionary to flatten.
        - keys (list): The list of keys representing the current path in the recursion.
        """
        for key, value in current_dict.items():
            if isinstance(value, dict):  
                flatten(value, keys + [key])
            else:  
                rows.append(keys + [key, value])

    flatten(nested_dict, parent_keys)

    column_names = [f"Level_{i}" for i in range(len(rows[0]) - 1)] + ["Value"]

    return pd.DataFrame(rows, columns=column_names)


def convert_keys_to_json_compatible(obj):
    """
    Recursively converts the keys of a dictionary to ensure JSON compatibility.

    This function processes dictionaries and lists, converting keys of type 
    `int` or `numpy.integer` to strings, as JSON keys must be strings. Nested
    dictionaries and lists are processed recursively.

    Parameters
    ----------
    obj : dict, list, or any
        The input object to be processed. It can be a dictionary, a list, or 
        any other type. If the object is not a dictionary or a list, it is 
        returned unchanged.

    Returns
    -------
    dict, list, or any
        The processed object with all dictionary keys converted to strings if 
        they were integers (`int` or `numpy.integer`). Lists and nested 
        structures are processed recursively.

    Examples
    --------
    >>> import numpy as np
    >>> data = {1: 'a', np.int32(2): {'nested': [3, 4]}, 'key': 'value'}
    >>> convert_keys_to_json_compatible(data)
    {'1': 'a', '2': {'nested': [3, 4]}, 'key': 'value'}

    >>> lst = [{'key': {42: 'answer'}}]
    >>> convert_keys_to_json_compatible(lst)
    [{'key': {'42': 'answer'}}]
    """
    if isinstance(obj, dict):
        return {
            str(k) if isinstance(k, (np.integer, int)) else k: convert_keys_to_json_compatible(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [convert_keys_to_json_compatible(i) for i in obj]
    else:
        return obj


def create_event (event_path, prefix):
    """
    Crea un evento con un nombre basado en un prefijo y un timestamp actual, 
    y genera una carpeta asociada al evento.

    Args:
        event_path (str): La ruta base donde se creará la carpeta del evento.
        prefix (str): El prefijo que se utilizará para nombrar el evento.

    Returns:
        tuple: Una tupla que contiene:
            - event (str): El nombre del evento generado, que consiste en el prefijo
              seguido de un timestamp con el formato 'YYYYMMDD_HHMMSS'.
            - event_folder_path (str): La ruta completa de la carpeta creada para el evento.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    event = f"{prefix}_{timestamp}"
    event_folder_path = crear_carpeta(event_path, event)
    return event, event_folder_path

def crear_carpeta(ruta_base, nombre_carpeta):
    """
    Crea una carpeta dada la ruta base y el nombre deseado

    Args:
        ruta_base(str): Ruta de la carpeta raíz
        nombre_carpeta(str): Nombre deseado para la carpeta
    Returns:
        str: Ruta completa de la carpeta creada
    """
    try:
        ruta_completa = os.path.join(ruta_base, nombre_carpeta)
        os.makedirs(ruta_completa, exist_ok=True)
        print(f"Carpeta creada en: {ruta_completa}")
        return ruta_completa
    except Exception as e:
        print(f"Ocurrió un error al crear la carpeta: {e}")

def save_array(path, file_name, array):
    """
    Guarda un array en formato .npy en la ruta especificada.

    Parámetros:
    path (str): La ruta completa, incluyendo el nombre del archivo donde se guardará el array.
    file_name (str): Nombre con el que se desea guardar el archivo
    array (numpy.ndarray): El array que se desea guardar.

    Ejemplo:
    save_array('ruta/al/archivo.npy', mi_array)
    """
    try:
        file_path = os.path.join(path, f'{file_name}.npy')
        np.save(file_path, array)
        print(f"Array guardado exitosamente en: {file_path}")
    except Exception as e:
        print(f"Error al guardar el array: {e}")

def read_codificated_csv(path):
    """
    Detecta la codificación del archivo .csv y lo lee utilizando esa codificación
    Args:
        path(str): Ruta al archivo .csv
    Returns:
        df(pd.DataFrame): Dataframe leído
    """
    with open(fr'{path}', 'rb') as f:
        result = chardet.detect(f.read())
    return pd.read_csv(fr'{path}', encoding=result['encoding'])