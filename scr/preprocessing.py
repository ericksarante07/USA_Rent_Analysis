import pandas as pd
import datetime


def prepare_dates (df):
    if 'date' not in df.columns:
        raise ValueError('La Columna date no esta en el dataframe o la misma no de llama asi.')
    
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'], format='%Y%m%d', errors='coerce')
    df_copy= df_copy[df_copy['date'].notna()]

    return df_copy 

def filter_units (df):
    if 'room_in_apt' not in df.columns:
        raise ValueError('La Columna room_in_apt no esta en el dataframe o la misma no de llama asi.')
    
    df_copy = df.copy()
    df_copy = df_copy[df_copy['room_in_apt'] == 0]

    return df_copy


def filter_cities (df, ciudad):
    if 'city' not in df.columns:
        raise ValueError('La Columna city no esta en el dataframe o la misma no de llama asi.')
    
    if not isinstance(ciudad, (list,tuple)) or len(ciudad)<=0:
        raise ValueError('ciudades debe de ser una lista o tuple con los nombre de las ciudades')
    
    ciudades_listado = set(df['city'].unique())
    si_ciudades = [x for x in ciudad if x in ciudades_listado]

    if len(si_ciudades)==0:
        raise ValueError(f"Ninguna de las ciudades solicitadas existe en el DataFrame: {ciudad}")

    df_copy = df.copy()
    df_copy = df_copy[df_copy['city'].isin(si_ciudades)]

    return df_copy

def product(df):
    if 'room_in_apt' not in df.columns:
        raise ValueError(' La Columna room_in_apt no esta en el dataset')
    
    df_copy = df.copy()
    df_copy['product'] = ['unit' if x == 0 else 'room' for x in df_copy['room_in_apt']]

    return df_copy

def clean_prices(df, p_low=0.01, p_high=0.99):
    if 'price' not in df.columns:
        raise ValueError("La columna 'price' no existe en el DataFrame")

    if not (0 < p_low < p_high < 1):
        raise ValueError("p_low y p_high deben cumplir 0 < p_low < p_high < 1")

    df_copy = df.copy()

    lower = df_copy['price'].quantile(p_low)
    upper = df_copy['price'].quantile(p_high)

    df_copy = df_copy[
        (df_copy['price'] >= lower) &
        (df_copy['price'] <= upper)
    ]

    return df_copy
    


def orquestador(df, ciudad, p_low=0.01, p_high=0.99):
    """
    Esta es la encargada de preparar los datos y quedarnos 
    con el producto unidad osea casa room_in_apt = 0

    :param df: dataframe
    :param cities: ciudades en lista
    :param p_low: rigor inferiro para outliers
    :param p_high: rigor superior para outliers

    """

    if df.empty:
        raise ValueError('El dataframe a venido vacio')
    
    df_copy=df.copy()

    df_fechas = prepare_dates(df_copy)

    df_units= filter_units(df_fechas)

    df_cities = filter_cities(df_units,ciudad=ciudad)

    df_prices = clean_prices(df_cities,p_low=p_low, p_high=p_high)

    return df_prices

def orquestador_unit_room (df, cities, p_low = 0.01, p_high=0.99):
    """
    Docstring for orquestador_unit_room
    
    Funcion que se queda con ambos productos  y crea columna identificandolos
    con un string

    :param df: dataframe
    :param cities: ciudades en lista
    :param p_low: rigor inferiro para outliers
    :param p_high: rigor superior para outliers
    """

    if df.empty:
        raise ValueError('El dataset es vacio')
    
    df_copy = df.copy()

    df_fechas = prepare_dates(df_copy)
    df_ciudad = filter_cities(df_fechas, cities)
    df_prices = clean_prices(df_ciudad, p_low=p_low, p_high=p_high)
    df_product = product(df_prices)

    return df_product