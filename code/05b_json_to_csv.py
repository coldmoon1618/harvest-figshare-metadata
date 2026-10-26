import pandas as pd
from pathlib import Path

input_json = Path.cwd().parent/'output'/'05a_harvested_full_metadata.json'
output_csv = Path.cwd().parent/'output'/'05b_harvested_full_metadata.csv'

df = pd.read_json(input_json)
df.to_csv(output_csv, index=False)
