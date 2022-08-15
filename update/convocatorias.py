#!/usr/bin/env python3

import pandas as pd
import unicodedata

def get_convocatorias():

    print('convocatorias')
    
    URL = "https://wsbt.ine.gob.bo/api/public/convocatorias/publicas/todos"
    nombres = {
        'BENI': 'beni',
        'CHUQUISACA': 'chuquisaca',
        'COCHABAMBA': 'cochabamba',
        'LA_PAZ': 'la_paz',
        'ORURO': 'oruro',
        'PANDO': 'pando',
        'POTOSI': 'potosi',
        'SANTA_CRUZ': 'santa_cruz',
        'TARIJA': 'tarija'
    }
    
    def consolidate_depto(convocatorias, dep):
        
        dep_convocatorias = convocatorias.groupby(['fecha_publicacion', 'referencia'])[dep].sum().reset_index()
        dep_convocatorias = dep_convocatorias.pivot_table(index='fecha_publicacion', columns='referencia', values=dep).fillna(0).astype(int)
        dep_convocatorias.insert(0, 'departamento', dep)
        return dep_convocatorias.reset_index()

    tabla = pd.read_json(URL)
    tabla = tabla[['fecha_publicacion', 'referencia', 'num_vacancia']]
    convocatorias = pd.DataFrame([{
        **row.to_dict(),
        **{i.replace("LA PAZ", "LA_PAZ").replace('SANTA CRUZ', 'SANTA_CRUZ').split(" ")[1]: i.split(" ")[0]
           for i in row["num_vacancia"].split(",")}}
        for i, row in tabla.iterrows()]).fillna(0)

    deptos = [col for col in convocatorias.columns if col not in tabla.columns]
    convocatorias[deptos] = convocatorias[deptos].astype(int)
    convocatorias = convocatorias.drop(columns="num_vacancia")
    convocatorias.referencia = convocatorias.referencia.str.lower().apply(lambda i: unicodedata.normalize('NFKD', i).encode('ascii', 'ignore').decode('ascii').replace(' ', '_'))
    convocatorias = convocatorias.rename(columns=nombres)
    
    deptos = [nombres[n] for n in nombres.keys()]
    total = convocatorias.groupby('referencia')[deptos].sum()
    convocatorias = pd.concat([consolidate_depto(convocatorias, dep) for dep in deptos]).sort_values(['departamento', 'fecha_publicacion'])
    
    return total, convocatorias

total, convocatorias = get_convocatorias()
total.to_csv('data/convocatorias_totales.csv')
convocatorias.to_csv('data/convocatorias.csv', index=False)
