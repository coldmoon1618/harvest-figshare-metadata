import csv
import json
import sys
import requests
from pathlib import Path

# Input and output
fIn   = Path.cwd().parent/'output'/'05b_harvested_full_metadata.csv'
fOut  = Path.cwd().parent/'output'/'05c_harvested_full_metadata_with_stats.csv'
fDict = Path.cwd().parent/'assets'/'domain_to_stats_dict.json'

# Configurations
user_input  = input('Starting index (press Enter for 0): ').strip()
start_index = int(user_input) if user_input else 0

mode = 'w' if start_index == 0 else 'a'
index = start_index

# Main code
csv.field_size_limit(10**9) # Handle large fields in the CSV

with open(fIn, newline='', encoding='utf-8') as f:
    harvested_items = list(csv.DictReader(f))
len_items = len(harvested_items)
print(f'{len_items} items to add stats')

with open(fDict, encoding='utf-8') as f:
    domain_to_stats = json.load(f)

new_cols = ['views_url', 'dnlds_url', 'cites_url', 'views', 'downloads', 'cites']
all_cols = list(harvested_items[0].keys()) + new_cols

def get_totals(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()['totals']

try:
    with open(fOut, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_cols)
        if start_index == 0:
            writer.writeheader()

        for index in range(start_index, len_items):
            item = harvested_items[index]
            print(f'\rStats harvest complete for item {index}',end='',flush=True)

            domain_url = item['figshare_url'].split('/articles/')[0].replace('https://', '')
            if domain_url not in domain_to_stats:
                sys.exit(f'\nStopped at item {index}: "{domain_url}" is not in the domain dictionary.\n'
                     f'Add it to assets/domain_to_stats_dict.json, then re-run with {index} as the starting index.')

            views_url  = domain_to_stats[domain_url] + item['id']
            dnlds_url  = views_url.replace('views', 'downloads')
            cites_url  = views_url.replace('views', 'cites')

            # prepare columns
            item['views_url'] = views_url
            item['dnlds_url'] = dnlds_url
            item['cites_url'] = cites_url
            # fetch responses
            item['views']     = get_totals(views_url)
            item['downloads'] = get_totals(dnlds_url)
            item['cites']     = get_totals(cites_url)

            writer.writerow(item)

except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
    print(f'\nStopped at item {index}: {type(e).__name__}')
    print(f'\nRe-run and enter {index} as the starting index to resume.')
else:
    print('\nAll items done.')
