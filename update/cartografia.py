#!/usr/bin/env python3
import pandas as pd
import datetime as dt
import os

def get_municipios():
    # url = 'tablaMunicipio.json'
    url = 'https://wsmon.ine.gob.bo/dashboard/tablaMunicipio'
    dfi = pd.read_json(url)
    return dfi

def get_timeline():
    # url = 'tablaFecha.json'
    url = 'https://wsmon.ine.gob.bo/dashboard/tablaFecha'
    dfi = pd.read_json(url)
    for col in ['fecha_inicio', 'fecha_final']:
        dfi[col] = pd.to_datetime(dfi[col])
    return dfi

def save_weekly(times):
    fn = 'data/cartografia/semanal.csv'
    t = times.copy()
    t.columns = ['departamento', 'fecha_inicio', 'fecha_final', 'viviendas']
    t.sort_values(['fecha_inicio', 'departamento']).to_csv(fn, date_format='%Y-%m-%d', index=False)

def save_state(mun):
    m = mun.copy()
    fn = 'data/cartografia/estado.csv'
    m.columns = ['departamento', 'provincia', 'municipio', 'viviendas']
    m.sort_values(['departamento', 'provincia', 'municipio']).to_csv(fn, index=False)

def save_daily(mun):
    fn = 'data/cartografia/diario.csv'
    m = mun.copy()
    m.columns = ['departamento', 'provincia', 'municipio', 'viviendas']
    ayer = dt.datetime.now().date() - dt.timedelta(days=1)
    daily = m.set_index(['departamento', 'provincia', 'municipio'])[['viviendas']].T
    daily.index = [ayer]
    if os.path.exists(fn):
        old = pd.read_csv(fn, header=[0,1,2], index_col=[0])
        daily = pd.concat([old, daily]).fillna(0).astype(int)
    daily.to_csv(fn)

def save_daily_aggregate(mun):
    fn = 'data/cartografia/timeline.csv'
    m = mun.copy()
    departamentos = {
        'chuquisaca': 'CHUQUISACA',
        'lapaz': 'LA PAZ',
        'cochabamba': 'COCHABAMBA',
        'oruro': 'ORURO',
        'potosi': 'POTOSI',
        'tarija': 'TARIJA',
        'santa': 'SANTA CRUZ',
        'beni': 'BENI',
        'pando': 'PANDO'
    }
    ayer = dt.datetime.now().date() - dt.timedelta(days=1)

    old = pd.read_csv('data/cartografia/old/presentacion.csv', parse_dates=['feccre'])
    old['feccre'] = old.feccre.dt.date
    old = old.rename(columns=departamentos).set_index('feccre')[departamentos.values()]
    old.index.name = 'fecha'
    old = old.sort_index().cumsum()

    new = pd.DataFrame([m.groupby('nombre').viviendas.sum().to_dict()])
    new.index = [ayer]

    timeline = pd.concat([old, new]).reset_index().drop_duplicates(subset=['index'], keep='last').set_index('index').sort_index()
    timeline.index.name = 'fecha'
    timeline.loc[:ayer].to_csv(fn)

mun = get_municipios()
times = get_timeline()

save_state(mun)
save_daily(mun)
save_weekly(times)
save_daily_aggregate(mun)