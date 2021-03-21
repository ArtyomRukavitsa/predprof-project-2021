import json


with open('20_years_format/Алмазный.json') as f:
    data = json.load(f)

for i in range(90, len(data), 365):
    print(data[i])