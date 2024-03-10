import json

with open("res", 'r') as f:
    lines = f.readlines()
data = {}
for line in lines:
    s = line.split("-")
    data[s[1].strip()] = s[0].strip()
with open("res.json", 'x') as f:
    json.dump(data, f)