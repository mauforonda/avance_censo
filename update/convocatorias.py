#!/usr/bin/env python3

import pandas as pd
import unicodedata

def get_convocatorias():

    print('convocatorias')
    
    URL = "https://wsbt.ine.gob.bo/api/public/convocatorias/publicas/todos"
    tabla = pd.read_json(URL)
    tabla = tabla[['fecha_publicacion', 'referencia', 'num_vacancia']]
    convocatorias = []
    for i, row in tabla.iterrows():
        for depto in row['num_vacancia'].split(','):
            demanda = int(depto.split(' ')[0])
            nombre = '_'.join(depto.strip().split(' ')[1:])
            convocatorias.append({'fecha_publicacion':row['fecha_publicacion'], 'departamento': nombre, 'referencia': row['referencia'], 'demanda': demanda})
            
    convocatorias = pd.DataFrame(convocatorias)
    for col in ['departamento', 'referencia']:
        convocatorias[col] = convocatorias[col].str.lower().apply(lambda i: unicodedata.normalize('NFKD', i).encode('ascii', 'ignore').decode('ascii').replace(' ', '_'))

    convocatorias = convocatorias.sort_values(['fecha_publicacion', 'departamento', 'referencia'])
    total = convocatorias.groupby(['departamento', 'referencia']).demanda.sum().reset_index().pivot_table(index='departamento', columns='referencia', values='demanda').fillna(0).astype(int)

    return total, convocatorias

total, convocatorias = get_convocatorias()
total.to_csv('data/convocatorias/convocatorias_totales.csv')
convocatorias.to_csv('data/convocatorias/convocatorias.csv', index=False)
