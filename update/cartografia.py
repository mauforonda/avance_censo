#!/usr/bin/env python3
import pandas as pd
import datetime as dt
import os
import requests

departamentos = [
    {'nombre': 'chuquisaca', 'codigo': 1},
    {'nombre': 'la_paz', 'codigo': 2},
    {'nombre': 'cochabamba', 'codigo': 3},
    {'nombre': 'oruro', 'codigo': 4},
    {'nombre': 'potosi', 'codigo': 5},
    {'nombre': 'tarija', 'codigo': 6},
    {'nombre': 'santa_cruz', 'codigo': 7},
    {'nombre': 'beni', 'codigo': 8},
    {'nombre': 'pando', 'codigo': 9}
]
resumen = []

def get_departamento(departamento):
    print('cartografia: {}'.format(departamento['nombre']))
    url = 'https://wsmon.ine.gob.bo/dashboard/tablaViviendas/{}'
    header = ['id_upm', 'codigo', 'departamento', 'provincia', 'municipio', 'area_censo', 'comunidad', 'zona', 'sector', 'area', 'viviendas_2012', 'viviendas_2022', 'fecha_aprobacion']
    response = requests.get(url.format(departamento['codigo']), timeout=40)
    if response.status_code == 200 and response.text != '[]':
        data = pd.DataFrame(response.json())
        # data = pd.read_json(url.format(departamento['codigo']))
        if data.shape[0] > 0:
            data = data.sort_values(['total_viv', 'total']).drop_duplicates(subset=['id_upm'], keep='last')
            data.columns = header
            data.departamento = departamento['nombre']
            for col in ['provincia', 'municipio']:
                data[col] = data[col].apply(lambda x: normalize(x))
            for col in ['viviendas_2012', 'viviendas_2022']:
                data[col] = data[col].astype(int)
            data.to_csv('data/cartografia/departamentos/{}.csv'.format(departamento['nombre']), index=False)
            resumen.append(data.groupby(['departamento', 'provincia', 'municipio'])[['viviendas_2012', 'viviendas_2022']].sum().reset_index())

def update_timeline(resumen):
    fn = 'data/cartografia/timeline.csv'
    fecha = dt.datetime.now().date() - dt.timedelta(days=1)
    timeline = resumen.set_index(['departamento', 'provincia', 'municipio'])[['viviendas_2022']].T
    timeline.index = [fecha]
    if os.path.exists(fn):
        old = pd.read_csv(fn, header=[0,1,2], index_col=[0])
        timeline = pd.concat([old, timeline]).fillna(0).astype(int)
    timeline.to_csv(fn)

def update_presentacion():
    url = 'https://wsmon.ine.gob.bo/dashboard/presentacionFecha'
    response = requests.get(url, timeout=40)
    if response.status_code == 200 and response.text != '[]':
        data = pd.DataFrame(response.json())
        data['feccre'] = pd.to_datetime(data.feccre)
        data.to_csv('data/cartografia/presentacion.csv', index=False)

def normalize(text):
    return text.lower().strip()

for departamento in departamentos:
    get_departamento(departamento)
resumen = pd.concat(resumen)
resumen.sort_values(['departamento', 'provincia', 'municipio']).to_csv('data/cartografia/resumen.csv', index=False)
update_timeline(resumen)
update_presentacion()
