import csv
import requests
import xmltodict
from pathlib import Path

# Output
out_path = Path.cwd().parent/'output' 
output   = out_path/'01a_portal_list.csv'

# Configurations 
token = "" # resumption token
portal_list = []
collecting_portals = False
base_url = 'https://api.figshare.com/v2/oai?verb=ListSets'

# Main code
while True:
    url = base_url + f'&resumptionToken={token}'
    response = requests.get(url)
    response.raise_for_status()
    data = xmltodict.parse(response.content)['OAI-PMH']

    items = data['ListSets']['set']
    token = data['ListSets'].get('resumptionToken', {}).get('#text', "")

    for item in items:
        if 'portal' in item['setSpec']:
            collecting_portals = True
            portal_id   = item['setSpec'].replace('portal_','')
            portal_name = item['setName']
            csv_item = {'portal_id': portal_id, 'portal_name': portal_name}
            portal_list.append(csv_item)
        elif collecting_portals:
            token = ''
            break

    if not token: #no more resumption token
        break

with open(output, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['portal_id', 'portal_name'], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(portal_list)

print(len(portal_list), 'portals saved')
