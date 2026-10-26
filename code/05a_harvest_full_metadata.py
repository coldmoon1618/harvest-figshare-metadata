import requests
import json
import os
from pathlib import Path

# Input and output
institutions_json= Path.cwd().parent/'output'/'03b_institutions_datasets_2022.json'  
figshare_json    = Path.cwd().parent/'output'/'04c_figshare_datasets_2022_sample3997.json'  
output_json      = Path.cwd().parent/'output'/'05a_harvested_full_metadata.json'
API_token_txt    = Path.cwd().parent/'assets'/'my_token.txt'

with open(institutions_json, 'r') as f:
    institutions_items = json.load(f)

with open(figshare_json, 'r') as f:
    figshare_items = json.load(f)

all_items = institutions_items + figshare_items
print(f'Total of {len(all_items)} items to harvest')

token_provided = False
if os.path.exists(API_token_txt):
    with open(API_token_txt, 'r') as f:
        my_token = f.read().strip()
        token_provided = True
        print('Token provided')

# Configurrations
user_input = input('Starting index (press Enter for 0): ').strip()
start_index= int(user_input) if user_input else 0

if start_index == 0:
    harvested_items = []
else:
    with open(output_json, 'r') as f:
        harvested_items = json.load(f)

index = start_index

# Main code
for item in all_items[start_index:]:
    try:
        if token_provided:
            response = requests.get(item['url_public_api'],
                                headers={'Authorization': f'token {my_token}'}, timeout=10)
        else:
            response = requests.get(item['url_public_api'], timeout=10)
        response.raise_for_status()
        harvested_items.append(response.json())

    except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
        api_message = None
        if hasattr(response, 'text') and response.text:
            try:
                json_response = response.json()
                if isinstance(json_response, dict) and "message" in json_response:
                    api_message = json_response["message"]
            except requests.exceptions.JSONDecodeError:
                pass
        
        if api_message:
            print(f'\nStopped at item {index}: {api_message}')
            print('Skipping this item')
            index += 1
            continue
        else:
            print(f'\nStopped at item {index}: {type(e).__name__}')
            if isinstance(e, requests.exceptions.HTTPError):
                print(f'HTTP Status: {response.status_code}, URL: {response.url}')
            break

    index += 1
    print(f'\rProcessing item {index}',end='',flush=True)

with open(output_json, 'w') as f:
    json.dump(harvested_items, f, indent=2)

# Rerun instructions
if index == len(all_items):
    print('\nAll done!')
else:
    print(f'\n{len(harvested_items)} items harvested and saved.')
    print(f'Re-run and enter {index} as the starting index to resume.')
