import json
import pandas as pd
from pathlib import Path

# Input and output
input_csv   = Path.cwd().parent/'output'/'02a_institutions_list_sorted.csv'
input_jsons = Path.cwd().parent/'output'/'03a_institutions_datasets'
output_json = Path.cwd().parent/'output'/'03b_institutions_datasets_2022.json'

# Main code
filtered_items = []
df = pd.read_csv(input_csv)
portal_id_list = df.iloc[:, 0].tolist()

for portal_id in portal_id_list:
    filename= f'institution_{portal_id}_datasets.json'
    fIn = input_jsons/filename
    try:
        with open(fIn) as f:
            items = json.load(f)
        counter = 0
        for item in items:
            if item['published_date'][:4] == '2022':
                filtered_items.append(item)
                counter += 1
        if counter > 0:
            print(f'{filename}: {counter} datasets added')
    except FileNotFoundError:
        print(f'{filename}: not found, skipping')

with open(output_json, 'w') as f:
    json.dump(filtered_items, f, indent=2)

print(f'{len(filtered_items)} total articles saved.')
