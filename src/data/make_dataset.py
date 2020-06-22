#!/usr/bin/python3

# Develop automated methods of collating papers that have used the tool and diversity statement (Python w/ CrossRef API using the Zenodo DOI https://zenodo.org/record/3672110).

# We plan to include an analysis of the collection of papers that use to code/diversity statement to compare their citation balance to a random selection of similar papers that do not.

import requests


def get_citations(doi):
    url = f'https://opencitations.net/index/coci/api/v1/citations/{doi}'
    items = requests.get(url).json()
    citing_dois = []
    for item in items:
        citing_dois.append(item['citing'])

    return citing_dois

dois_citing_paper = get_citations(doi='10.1101/2020.01.03.894378')
dois_citing_code = get_citations(doi='10.5281/zenodo.3672109')
