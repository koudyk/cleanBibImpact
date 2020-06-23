#!/usr/bin/python3

# Develop automated methods of collating papers that have used the tool and diversity statement (Python w/ CrossRef API using the Zenodo DOI https://zenodo.org/record/3672110).

# We plan to include an analysis of the collection of papers that use to code/diversity statement to compare their citation balance to a random selection of similar papers that do not.

import requests
from habanero import Crossref
import numpy as np
import pandas as pd
np.random.seed(seed=93287583)

GENDER_API_KEY = open('gender_api_key.txt', 'r').read().strip()


def git_citing_dois(doi):
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


def name_to_gender(name, api_key=GENDER_API_KEY):
    url = f'https://gender-api.com/get?key={api_key}&name={name}'
    response = requests.get(url).json()
    gender = response['gender']
    accuracy = response['accuracy']
    return gender, accuracy


def get_data(df):
    '''
    For each doi in a dataframe containing a column called 'doi',
    get the names, genders, and gender accuracies of the first and last
    authors
    '''
    for n, doi in enumerate(df['doi']):
        print('\tDOI %d / %d\r' % (n, len(citing_papers)), end='')
        fa_name, la_name = names_from_xref(doi)
        fa_gender, fa_accuracy = name_to_gender(fa_name)
        la_gender, la_accuracy = name_to_gender(la_name)

        df.at[n, 'first_author_name'] = fa_name
        df.at[n, 'first_author_gender'] = fa_gender
        df.at[n, 'first_author_gender_accuracy'] = fa_accuracy

        df.at[n, 'last_author_name'] = la_name
        df.at[n, 'last_author_gender'] = la_gender
        df.at[n, 'last_author_gender_accuracy'] = la_accuracy
    print('\n')
    return df


# get the data for the citing papers
citing_papers = pd.DataFrame()

print('\nLooking for DOIS for the citing papers\n')
# code_doi = '10.5281/zenodo.3672109'
# NOTE - use the code_doi when there are enough papers citing it
paper_doi = '10.1101/2020.01.03.894378'
citing_papers['doi'] = git_citing_dois(paper_doi)

print('\nLooking for author names and genders for the citing papers\n')
citing_papers = get_data(citing_papers)

datafile = '../../data/citing_papers.csv'
print(f'\nSaving data to {datafile}\n')
citing_papers.to_csv(datafile)
