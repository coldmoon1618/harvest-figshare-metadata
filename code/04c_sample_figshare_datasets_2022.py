import json
import random
from pathlib import Path

institutions_json= Path.cwd().parent/'output'/'03b_institutions_datasets_2022.json'  
figshare_json    = Path.cwd().parent/'output'/'04b_figshare_datasets_2022.json'  
output_path      = Path.cwd().parent/'output'

with open(institutions_json,'r') as f:
    institutions_items = json.load(f)

sample_size = len(institutions_items)

with open(figshare_json, 'r') as f:
    figshare_items = json.load(f)

sample = random.sample(figshare_items, sample_size)

with open(output_path/f'04c_figshare_datasets_2022_sample{sample_size}.json', 'w') as f:
    json.dump(sample, f, indent=2)

print(f'{len(sample)} items sampled from {len(figshare_items)} and saved.')
