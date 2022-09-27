#!/usr/bin/env python3
import pandas as pd
import datetime as dt
import os

def get_municipios():
    url = 'https://wsmon.ine.gob.bo/dashboard/tablaMunicipio'
    dfi = pd.read_json(url)
    return dfi

def get_timeline():
    url = 'https://wsmon.ine.gob.bo/dashboard/tablaFecha'
    dfi = pd.read_json(url)
    for col in ['fecha_inicio', 'fecha_final']:
        dfi[col] = pd.to_datetime(dfi[col])
    return dfi

def save_weekly(times):
    fn = 'data/cartografia/semanal.csv'
    times.columns = ['departamento', 'fecha_inicio', 'fecha_final', 'viviendas']
    times.to_csv(fn, date_format='%Y-%m-%d', index=False)

def save_state(mun):
    fn = 'data/cartografia/estado.csv'
    mun.columns = ['departamento', 'provincia', 'municipio', 'viviendas']
    mun.to_csv(fn, index=False)

def save_daily(mun):
    fn = 'data/cartografia/diario.csv'
    mun.columns = ['departamento', 'provincia', 'municipio', 'viviendas']
    ayer = dt.datetime.now().date() - dt.timedelta(days=1)
    daily = mun.set_index(['departamento', 'provincia', 'municipio'])[['viviendas']].T
    daily.index = [ayer]
    if os.path.exists(fn):
        old = pd.read_csv(fn, header=[0,1,2], index_col=[0])
        daily = pd.concat([old, daily]).fillna(0).astype(int)
    daily.to_csv(fn)

mun = get_municipios()
times = get_timeline()

save_state(mun)
save_daily(mun)
save_weekly(times)