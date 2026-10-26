import json
import requests
import pandas as pd
from pathlib import Path

# Input and output
input_csv = Path.cwd().parent/'output'/'02a_institutions_list_sorted.csv' 
out_path  = Path.cwd().parent/'output'/'03a_institutions_datasets'
out_path.mkdir(parents=True, exist_ok=True)

# Configurations 
base_url  = 'https://api.figshare.com/v2/articles'
page_size = 1000

user_input  = input('Starting index (press Enter for 0): ').strip()
start_index = int(user_input) if user_input else 0

# Main code
df = pd.read_csv(input_csv)
portal_id_list = df.iloc[:, 0].tolist()
print(f'Total of {len(portal_id_list)} institutions to download from')

def get_institutions_articles(portal_id):
  print(f'\nStarting institution {portal_id} (index={institution_index})')
  all_items = []
  page = 1

  while True:
      try:
          response = requests.get(base_url,
                                  params={'institution': portal_id,
                                          'page_size': page_size,
                                          'page': page,
                                          'item_type': 3, # 3 stands for dataset
                                          'order':'published_date',
                                          'order_direction':'asc',
                                          'published_since':'2022-01-01'})
          items = response.json()

          # Two behaviors of reaching the limit
          # 1) Empty list
          if not items:
              break
          # 2) Explicit message
          # {"message": "Your requested offset (11000) exceeds the maximum accepted offset (10000)",
          # "code": "PaginationOffsetExceeded"}
          if "message" in items:
              break

          all_items.extend(items)
          print(f'\rCollected {len(all_items)} dataset articles across {page} page(s)',end='',flush=True)
          page += 1

      except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
          print(f'\nStopped at index {institution_index}: {type(e).__name__}')
          return False # Institution incomplete

  with open(out_path/f'institution_{portal_id}_datasets.json', 'w') as fOut:
      json.dump(all_items, fOut, indent=2)

  return True #success

for portal_id in portal_id_list[start_index:]:
    institution_index = portal_id_list.index(portal_id)
    success = get_institutions_articles(portal_id)
    if not success:
        print('\nDownload interrupted.')
        break
    else:
        print('\nDownload complete.')

# Rerun instructions
if institution_index == len(portal_id_list)-1:
    print('\nAll done!')
else:
    print(f'\nDone up to index {institution_index}. Enter {institution_index} as the starting index in the next run.')
