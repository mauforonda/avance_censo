#!/usr/bin/env python3

import pandas as pd
import datetime as dt
import pytz

"""
Descarga el número de áreas de trabajo en proceso o concluídas 
en la actualización cartográfica estadística por municipio.
"""

DIRECTORY = 'data/cartografia'
URL = "https://sigedv2.ine.gob.bo/geoserver/ows?service=WFS&request=GetFeature&typeName=seguimiento:vw_ac_2021_cartografia&outputFormat=csv"
RELEVANT_COLUMNS = ["codigo","sectores_ace","sector"]

ayer = dt.datetime.now(tz=pytz.timezone('America/La_Paz')).replace() - dt.timedelta(days=1)
df = pd.read_csv(URL)[RELEVANT_COLUMNS]
df.insert(0, 'fecha', ayer)

total = df[['codigo', 'sectores_ace']]
total.to_csv(
    f'{DIRECTORY}/areas_totales.csv',
    header=['codigo_municipio', 'areas'],
    date_format='%Y-%m-%d',
    index=False
)

avance_filename = f'{DIRECTORY}/areas_concluidas_o_en_proceso.csv'
avance = df[['fecha', 'codigo', 'sector']]
avance.columns = ['fecha', 'codigo_municipio', 'areas']
avance = pd.concat([
    pd.read_csv(avance_filename, parse_dates=['fecha']),
    avance
])
avance.to_csv(
    avance_filename,
    header=['fecha', 'codigo_municipio', 'areas'],
    date_format='%Y-%m-%d',
    index=False
)
