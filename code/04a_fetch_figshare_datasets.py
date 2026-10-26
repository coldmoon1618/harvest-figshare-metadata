'''
This time pagination limit matters because the search shows 23k datasets
https://figshare.com/search?itemTypes=3&sources=figshare.com&publicationYears=2022
Start with 2022-01-01 and then proceed as instructed
WARNING: this does create duplicates when you resume from a previous date
04b_filter_figshare_datesets.py will filter by year and remove duplicate
'''
import json
import requests
from pathlib import Path

# Output
output_json = Path.cwd().parent/'output'/'04a_figshare_datasets_with_duplicates.json'

# Configurations
base_url = 'https://api.figshare.com/v2/articles'
page_size = 1000

start_date = input('Starting date (press Enter for 2022-01-01): ').strip()
start_date = start_date if start_date else '2022-01-01'
user_input = input('Starting page (press Enter for 1): ').strip()
start_page = int(user_input) if user_input else 1

if start_date == '2022-01-01' and start_page == 1:
    all_items = []
else:      
    with open(output_json) as f:
        all_items = json.load(f)

# Main code
page = start_page
end_reached = False

while True:
    if "message" in all_items:
        print(f'Reached the end at page {page}')
        break
    try:
        response = requests.get(base_url, 
                                params={'institution': 0, # For plain figshare
                                        'page_size': page_size,
                                        'page': page,
                                        'item_type': 3, # 3 stands for dataset
                                        'order':'published_date',
                                        'order_direction':'asc',
                                        'published_since':start_date})
        items = response.json()
        response.raise_for_status()

        # {"message": "Your requested offset (11000) exceeds the maximum accepted offset (10000)",
        # "code": "PaginationOffsetExceeded"}
        if "message" in items:
            print(f'Reached the end at page {page}')
            end_reached = True
            break

        all_items.extend(items)
        print(f'\rpage {page} ({len(all_items)} articles so far)',end='',flush=True)
        page += 1

    except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
        print(f'\nStopped at page {page}: {type(e).__name__}')
        break

with open(output_json, 'w') as f:
    json.dump(all_items, f, indent=2)
latest_date = all_items[-1]['published_date'].split('T')[0]

print(f'\n{len(all_items)} articles saved. The last one was published on {latest_date}.')

# Rerun instructions
if end_reached:
    start_date = latested_date
    page = 1
print('\nUse the following parameters for the next run:')
print(f'Starting date: {start_date}')
print(f'Starting page: {page}')
