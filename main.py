import pandas as pd 
from scr.preprocessing import orquestador, orquestador_unit_room

CITIES = ['san francisco', 'oakland', 'alameda', 'berkeley']

def main():
    df = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2022/2022-07-05/rent.csv')

    df_precio = orquestador(df, CITIES)
    
    df_producto = orquestador_unit_room(df, CITIES)
    
    df_precio.to_csv(
        'data/processed/rent_unit.csv',
        index=False
    )
    df_producto.to_csv(
        'data/processed/rent_unit_room.csv',
        index=False
    )

    print('Datasets procesados correctamente')


if __name__ == '__main__':
    main() 