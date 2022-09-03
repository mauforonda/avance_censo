#!/usr/bin/env python3

import requests
import pandas as pd
import json

url = "https://seguimiento.ine.gob.bo/api/v3/queries/default?pageSize=500&columns%5B%5D=type&columns%5B%5D=id&columns%5B%5D=subject&columns%5B%5D=status&timelineVisible=true&timelineLabels=%7B%22left%22%3A%22startDate%22%2C%22right%22%3A%22dueDate%22%2C%22farRight%22%3Anull%7D&timelineZoomLevel=auto&highlightingMode=none&showHierarchies=false&groupBy=project&filters=%5B%7B%22project%22%3A%7B%22operator%22%3A%22%3D%22%2C%22values%22%3A%5B%225%22%5D%7D%7D%5D&sortBy=%5B%5B%22id%22%2C%22asc%22%5D%5D&offset=1"
columnas = ['id', 'derivedStartDate', 'derivedDueDate', 'subject', 'description.raw', '_links.status.title', 'percentageDone', '_links.children']
names = ['id', 'start', 'end', 'subject', 'description', 'status', 'percent', 'children']

response = requests.get(url)
df = pd.json_normalize(response.json()['_embedded']['results']['_embedded']['elements'])[columnas]
df['_links.children'] = df['_links.children'].apply(lambda x: [i['href'].split('/')[-1] for i in x] if type(x) == list else None)
df.columns = names
df = df.sort_values(['id'])
with open('data/cronograma/cronograma.json', 'w+') as f: 
    json.dump(df.set_index('id').to_dict(orient='index'), f, ensure_ascii=False)