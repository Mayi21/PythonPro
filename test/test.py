import json

with open('USA.json', 'r') as f:
    data = json.load(f)
for d in data['features']:
    print(d['properties']['name'].strip())
