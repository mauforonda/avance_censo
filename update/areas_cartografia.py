#!/usr/bin/env python3

import pandas as pd
import datetime as dt
import pytz

"""
Descarga el número de áreas de trabajo en proceso o concluídas 
en la actualización cartográfica estadística por municipio.
"""

DIRECTORY = 'data/cartografia'
URL = "https://sigedv2.ine.gob.bo/geoserver/ows?service=WFS&request=GetFeature&typeName=DASHBOARD:vw_municipio_proyeccion_sector_221122&outputFormat=csv"
RELEVANT_COLUMNS = ["codigo","total_gral","concluido"]

ayer = dt.datetime.now(tz=pytz.timezone('America/La_Paz')).replace() - dt.timedelta(days=1)
df = pd.read_csv(URL)[RELEVANT_COLUMNS]
df.insert(0, 'fecha', ayer)

total = df[['codigo', 'total_gral']]
total.to_csv(
    f'{DIRECTORY}/areas_totales.csv',
    header=['codigo_municipio', 'areas'],
    index=False
)

avance_filename = f'{DIRECTORY}/areas_concluidas_o_en_proceso.csv'
avance = df[['fecha', 'codigo', 'concluido']]
avance.columns = ['fecha', 'codigo_municipio', 'areas']
avance = pd.concat([
    pd.read_csv(avance_filename, parse_dates=['fecha']),
    avance
])
avance.fecha = avance.fecha.apply(lambda x: x.strftime('%Y-%m-%d'))
avance.to_csv(
    avance_filename,
    index=False
)
