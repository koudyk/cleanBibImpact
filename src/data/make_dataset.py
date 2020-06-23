#!/usr/bin/python3

# Develop automated methods of collating papers that have used the tool and diversity statement (Python w/ CrossRef API using the Zenodo DOI https://zenodo.org/record/3672110).

# We plan to include an analysis of the collection of papers that use to code/diversity statement to compare their citation balance to a random selection of similar papers that do not.

import requests
from habanero import Crossref
import numpy as np
np.random.seed(seed=93287583)


def get_citations(doi):
    '''
    Get the dois of papers citing a given doi using opencitations.net

    Silvio Peroni, David Shotton (2020). OpenCitations, an infrastructure
    organization for open scholarship. Quantitative Science Studies, 1(1):
    428-444. https://doi.org/10.1162/qss_a_00023
    '''
    url = f'https://opencitations.net/index/coci/api/v1/citations/{doi}'
    items = requests.get(url).json()
    citing_dois = []
    for item in items:
        citing_dois.append(item['citing'])

    return citing_dois


def get_name_from_author_dict(author_dict):
    if 'given' not in author_dict:
        name = ''
    else:
        # trim initials
        name = author_dict['given'].replace('.', ' ').split()[0]
    return name


def names_from_xref(doi):
    '''
    Get the first names of the first and last authors for a given DOI
    '''
    cr = Crossref()
    title = ''
    works = cr.works(query=title, select=["DOI", "author"], limit=1,
                     filter={'doi': doi})
    if works['message']['total-results'] > 0:
        item = works['message']['items'][0]
        if 'author' in item.keys():
            first_author = get_name_from_author_dict(item['author'][0])
            last_author = get_name_from_author_dict(item['author'][-1])
        else:
            first_author = ''
            last_author = ''
    return first_author, last_author


# get dois for papers citing the original paper and the code,
print('\nLooking for DOIS for the citing papers\n')
code_doi = '10.5281/zenodo.3672109'
paper_doi = '10.1101/2020.01.03.894378'
dois_citing_paper = get_citations(paper_doi)}

# get random DOIs
# TODO check they're not in the list of citing dois
# TODO check that the results are papers
# TODO make recent time range
# TODO limit to neuroscience
# print('\nLooking for DOIS for random papers\n')
# cr = Crossref()
# n_samples = 10
# n_random_dois = len(dois['paper']) * n_samples
# random_dois = cr.random_dois(n_random_dois)

# get the first and last names for dois
print('Looking for author names for the citing papsers')
citing_first_authors = []
citing_last_authors = []
for n, doi in enumerate(doi_list):
    print('\tDOI %d / %d\r' %(n, len(doi_list) - 1), end='')
    citing_first_authors.append(names_from_xref(doi)[0])
    citing_last_authors.append(names_from_xref(doi)[1])
    print('\n')
