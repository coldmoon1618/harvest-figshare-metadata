import csv
import requests
from pathlib import Path

# Input and output
out_path    = Path.cwd().parent / 'output' 
input_csv   = out_path/'01a_portal_list.csv'
output_csv  = out_path/'01b_portal_list_enriched.csv'

# Configurations
user_input  = input('Starting index (press Enter for 0): ').strip()
start_index = int(user_input) if user_input else 0
mode = 'w' if start_index == 0 else 'a'

# Main code
with open(input_csv, newline='', encoding='utf-8') as f:
    portal_list = list(csv.DictReader(f))

with open(output_csv, mode, newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['portal_id', 'portal_name', 'portal_url','example_article'])
    if mode == 'w':
        writer.writeheader()

    stop_index = len(portal_list)

    for i in range(start_index, len(portal_list)):
        portal = portal_list[i]
        print(f'\rProcessing index {i}',end='',flush=True)
        try:
            response = requests.get(f'https://api.figshare.com/v2/articles?institution={portal["portal_id"]}&limit=1')
            response.raise_for_status()
            data = response.json()

            if len(data) == 0:
                portal['portal_url'] = 'INVALID_no_article_published'
                portal['example_article'] = 'INVALID_no_article_published'
            else:
                portal['portal_url'] = data[0]['url_public_html'].replace('https://', '').split('/')[0]
                portal['example_article'] = data[0]['id']

            writer.writerow(portal)

        except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
            print(f'\nStopped at item {i}: {type(e).__name__}')
            stop_index = i
            break
if stop_index == len(portal_list):
    print('\nAll done.')
else:
    print(f'\nDone up to index {stop_index}. Enter {stop_index} as the starting index in the next run.')
