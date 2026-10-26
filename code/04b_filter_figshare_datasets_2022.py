import json
from pathlib import Path

input_json  = Path.cwd().parent/'output'/'04a_figshare_datasets_with_duplicates.json'
output_json = Path.cwd().parent/'output'/'04b_figshare_datasets_2022.json'

with open(input_json,'r') as fIn:
    all_items = json.load(fIn)

filtered_items = []
article_id_set = set()

print('Removing duplicates from:')
for item in all_items:
    if item['id'] in article_id_set:
        print(item['published_date'])
        continue
    if item['published_date'][:4] == '2022':
        article_id_set.add(item['id'])
        filtered_items.append(item)

with open(output_json, 'w') as fOut:
    json.dump(filtered_items, fOut, indent=2)
print(f'\n{len(filtered_items)} unique datasets saved')
