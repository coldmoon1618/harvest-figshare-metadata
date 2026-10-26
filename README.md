# README

## GENERAL INFORMATION

### REPOSITORY TITLE

Code for Harvesting Full Metadata on All Datasets Published on Figshare in 2022

### REPOSITORY URL
[https://github.com/coldmoon1618/harvest-figshare-metadata](https://github.com/coldmoon1618/harvest-figshare-metadata)

### REPOSITORY ABSTRACT

This repository contains the code to obtain full metadata on all datasets published on Figshare.com and Figshare institutional repositories in 2022. This code can be easily modified in parts for studies that require bulk harvesting of full metadata with a particular selection of interest (such as institution, time period, or a Figshare article type). Notably, the code handles different types of API interruptions, allows keyboard interruption, and provides instructions to rerun the code to resume the progress. This repository also provides a lookup table for Figshare usage statistics endpoints.

### AUTHOR

- Yunxiao "Michelle" Zhai
	- ORCID: 0000-0001-7207-5122
	- Institution: Iowa State University Library
	- Email: zhai@iastate.edu
	- GitHub: github.com/coldmoon1618

### DEVELOPMENT INFORMATION
- The code was first developed in September and October of 2026.
- Demo metadata and usage statistics were harvested in the first week of October 2026.

### ASSOCIATED PUBLICATION AND ACKNOWLEDGEMENT
- This repository will also be included in an upcoming dataset publication associated with an upcoming paper (_the paper_). The preprint of _the paper_ is available at [https://hdl.handle.net/10919/143106](https://hdl.handle.net/10919/143106).
- Even though this repository was completely rewritten from scratch, it was initially an attempt to streamline the workflow used in the [figshare_API_data_use_metrics](https://github.com/VTUL/figshare_API_data_use_metrics) repository. The `figshare_API_data_use_metrics` repository produced the original results used in _the paper_. This repository also extracted the the [link](https://api.figshare.com/v2/oai?verb=ListSets) to fetch all Figshare portals.
- The URL links in `domain_to_stats_dict.json` were compiled from information gathered by Padma Carstens and Jonathan Petters, which will be part of the upcoming dataset publication. 
- The list `02a_institutions_list_sorted.csv` reflects the selection of institutions used in _the paper_. 

## FILE DIRECTORY

### WORKFLOW

The code and output from the code have been named according to the overall workflow steps behind _the paper_, which can be summarized as below:

1. Obtain a full list of Figshare portals, some of which are institutional repositories  
2. Manually select institutions from the full list of portals using criteria
3. Obtain a list of datasets published in 2022 and hosted on institutional repositories (_institutions datasets_) 
4. Obtain a list of datasets published in 2022 and hosted on Figshare.com (_figshare datasets_) 
5. Harvest complete metadata and stats for selected datasets from both Step 3 and Step 4 
6. Manually select datasets from the harvested datasets using criteria

### DIRECTORY OVERVIEW
```
.
├── README.md
├── LICENSE
├── code
│   ├── 01a_fetch_portal_list.py
│   ├── 01b_append_portal_info.py
│   ├── 03a_fetch_institutions_datasets.py
│   ├── 03b_filter_institutions_datasets_2022.py
│   ├── 04a_fetch_figshare_datasets.py
│   ├── 04b_filter_figshare_datasets_2022.py
│   ├── 04c_sample_figshare_datasets_2022.py
│   ├── 05a_harvest_full_metadata.py
│   ├── 05b_json_to_csv.py
│   └── 05c_append_stats.py
├── assets
│   ├── my_token.txt (NOT PROVIDED)
│   └── domain_to_stats_dict.json
└── output
    ├── 01a_portal_list.csv
    ├── 01b_portal_list_enriched.csv
    ├── 02a_institutions_list_sorted.csv
    ├── 03a_institutions_datasets/institution_{id}_datasets.json
    ├── 03b_institutions_datasets_2022.json
    ├── 04a_figshare_datasets_with_duplicates.json
    ├── 04b_figshare_datasets_2022.json
    ├── 04c_figshare_datasets_2022_sample3997.json
    ├── 05a_harvested_full_metadata.json
    ├── 05b_harvested_full_metadata.csv
    └── 05c_harvested_full_metadata_with_stats.csv
```

### DIRECTORY: CODE

#### Context
There are generally two types of API interruptions:
- Figshare imposes an API limit by time and hit that will return 403 error when exceeded
- Figshare imposes a pagination limit at a maximum of 10,000 items per query (_10k limit_)

#### Files
- `01a_fetch_portal_list.py`
	- Obtains a full list of portals provided by Figshare.
	- Source: [https://api.figshare.com/v2/oai?verb=ListSets](https://api.figshare.com/v2/oai?verb=ListSets)
	- Output: `01a_portal_list.csv` 
- `01b_append_portal_info.py`
	- Append additional information on the portals. While this additional information is not used in the following code, it is used for manually checking the sites and can be used to check the usage statistics endpoints in `assets/domain_to_stats_dict.json`. 
	- Input: `01a_portal_list.csv`
	- Output: `01b_portal_list_enriched.csv`
- `03a_fetch_institutions_datasets.py` 
	- Loop through the sorted listed and obtain one list per institution of datasets published on institution repositories since 2022-01-01.
	- Source: `https://api.figshare.com/v2/articles`
	- Input: `02a_institutions_list_sorted.csv`
	- Output: `03a_institutions_datasets/institution_{id}_datasets.json`
- `03b_filter_institutions_datasets_2022.py`
	- Select only the datasets published in 2022 and compile them into one JSON file.
	- Input: `03a_institutions_datasets/institution_{id}_datasets.json`
	- Output: `03b_institutions_datasets_2022.json`
- `04a_fetch_figshare_datasets.py`
	- Obtain a list of datasets hosted on figshare.com published since 2022-01-01. Due to the 10k limit, the code needs to be run at least 3 times to grab [all 23k datasets hosted by Figshare in 2022](https://figshare.com/search?itemTypes=3&sources=figshare.com&publicationYears=2022). 
	- Warning: This creates duplicates, which are filtered out by `04b_filter_figshare_datasets_2022.py`.
	- Alternative usage: You can change the institution ID from 0 to the institution of interest if you are only interested in querying one institution, such as your home institution.
	- Source: `https://api.figshare.com/v2/articles`
	- Output: `04a_figshare_datasets_with_duplicates.json`
- `04b_filter_figshare_datasets_2022.py`
	- Removes duplicates created by `04a_fetch_figshare_datasets.py` and selects only the datasets published in 2022.
	- Input: `04a_figshare_datasets_with_duplicates.json`
	- Output: `04b_figshare_datasets_2022.json`
- `04c_sample_figshare_datasets_2022.py`
	- Randomly sample the same number of Figshare datasets as institution datasets
	- Input: `04b_figshare_datasets_2022.json`
	- Output: `04c_figshare_datasets_2022_sample3997.json`
- `05a_harvest_full_metadata.py`
	- Harvest full metadata from the lists of datasets
	- Input1: `03b_institutions_datasets_2022.json`
	- Input2: `04c_figshare_datasets_2022_sample3997.json`
	- Output: `05a_harvested_full_metadata.json`
- `05b_json_to_csv.py`
	- Naively converts JSON to CSV. You can customize this code by editing the columns of interest or performing additional JSON parsing.	
	- Input: `05a_harvested_full_metadata.json`
	- Output: `05b_harvested_full_metadata.csv`
- `05c_append_stats.py`
	- Appends usage statistics to the CSV file 
	- Dependency: `assets/domain_to_stats_dict.json`
	- Optional: `assets/my_token.txt`
	- Source: https://stats.figshare.com
	- Input: `05b_harvested_full_metadata.csv`
	- Output: `05c_harvested_full_metadata_with_stats.csv`

### DIRECTORY: ASSETS

#### Context
For Figshare datasets, the usage statistics can be obtained by 
```
https://stats.figshare.com/total/{metrics}/article/{article_id}
``` 
where `metrics` options are `views`, `downloads`, and `cites`. The complication comes in for institution datasets, where the default endpoint gives 0 for all counts without raising errors. To obtain the correct stats, the endpoint is 
```
https://stats.figshare.com/{custom_endpoint}/total/{metric}/article/{article_id}
``` 
where `custom_endpoint` is not always trivial to obtain and sometimes required manual inquiry by Padma and Jonathan. The resulting list is now compiled in a Python dictionary `domain_to_stats_dict.json` that users can use and append to for easy lookup.

#### Files
- `domain_to_stats_dict.json`
  	- Python dictionary to look up the Figshare statistics endpoint for the number of views. Users can append to this dictionary if the institution of interest is not included
  	- The custom domain here corresponds to `portal_url`
- `my_token.txt`
	- NOT provided in this repository	 
	- Providing a Figshare API token allows a higher query limit before hitting a 403 error and grants permissions for queries that .
	- Users are encouraged to obtain a [Figshare API token](https://info.figshare.com/user-guide/how-to-get-a-personal-token/) and store the string in this file.
	
### DIRECTORY: OUTPUT

#### Files
- `01a_portal_list.csv`
	- Columns: `portal_id`, `portal_name`
	- Row count: 272 
- `01b_portal_list_enriched.csv`
	- Columns: `portal_id`, `portal_name`, `portal_url`, `example_article`
	- Row count: 272
- `02a_institutions_list_sorted.csv`
	- Columns: `institution_id`, `InstitutionName`, `CustomDomain`, `example_article`
	- Row count: 111
	- Sorted by ascending institution ID assigned by Figshare, manually filtered by Jonathan and Megan to exclude publishers, societies, presses, conference sites, preprint servers and `datasets` items that aren't actually datasets.
- `03a_institutions_datasets/institution_{id}_datasets.json`
	- Lists of datasets, one per institution, published on institution repositories since 2022-01-01. The 10k limit far exceeds any dataset count hosted by an institution repository in 2022.
	- Total of 111 files
- `03b_institutions_datasets_2022.json`
	- All datasets published on institution repositories in 2022.
	- Total of 3,997 Figshare articles
- `04a_figshare_datasets_with_duplicates.json`
	- A list of 30k datasets including duplicates and datasets outside of 2022.
- `04b_figshare_datasets_2022.json`
	- Datasets published in 2022 on Figshare, a total of 23,041 Figshare articles. 
- `04c_figshare_datasets_2022_sample3997.json`
	- Example random sample, which differs from the sample used in _the paper_.
- `05a_harvested_full_metadata.json`
	- Demonstration file using every 10th item as proof of concept, a total of 799 Figshare articles. 
- `05b_harvested_full_metadata.csv`
	- Naively converted to CSV from `05a_harvested_full_metadata.json`, where cell contents are still formatted in JSON syntax.
	- Row count: 799
- `05c_harvested_full_metadata_with_stats.csv`
	- Includes 6 extra columns: `views_url`, `dnlds_url`, `cites_url`, `views`, `downloads`, `cites`
	- Row count: 799

## SOFTWARE
### Development
- The code was initially developed in Google Colab and tested on macOS in September and October of 2026.
- The demo metadata and usage statistics were harvested in Google Colab.
- Claude Sonnet 5.5 was used in coding assistance such as explaining concepts, catching exceptions, and handling resumption indices. 

### Python requirements

```
requires-python = ">=3.14"
dependencies = [
    "pandas>=3.0.6",
    "requests>=2.34.2",
    "xmltodict>=1.0.4",
]
```
## LICENSE
MIT
Copyright (c) 2026 Yunxiao "Michele" Zhai, Iowa State University

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
