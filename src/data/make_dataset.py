import requests
import sys
import os
import json
from habanero import Crossref
import numpy as np
import pandas as pd
import gender_guesser.detector as gender_detecor


# Relative paths from src/data
GENDER_API_KEY_PATH = "gender_api_key.txt"
NAME_DICT_PATH = "name_dict.json"
DATAFILE_PATH = "../../data/citing_papers.csv"

# list the cited dois. we're interested in which papers cite these dois
CITED_DOIS = {
    "paper": "10.1038/s41593-020-0658-y",
    "preprint": "10.1101/2020.01.03.894378",
    "code": "10.5281/zenodo.3672109",
}


def get_dois(doi, citing=True):
    """
    Get the dois of papers citing or cited by a given doi using opencitations.net

    Silvio Peroni, David Shotton (2020). OpenCitations, an infrastructure
    organization for open scholarship. Quantitative Science Studies, 1(1):
    428-444. https://doi.org/10.1162/qss_a_00023


    Inputs
    ------
    doi : string
        The DOI of the paper whose citing DOIs or references you want to list.
    citing : bool,
        Wether to get the DOIs citing the given DOI or cited by the given DOI (default: True).

    Outputs
    -------
    citing_dois : list of strings
        List of DOIs of papers that cite the given DOI.
    """
    type = "citations" if citing else "references"
    key = "citing" if citing else "cited"
    url = f"https://opencitations.net/index/coci/api/v1/{type}/{doi}"
    items = requests.get(url).json()
    found_dois = []
    if items:  # if opencitations.net lists citing items
        for item in items:
            found_dois.append(item[key])
    return found_dois


def get_name_from_author_dict(author_dict):
    """
    This function


    Inputs
    ------
    author_dict : dict
        Dictionary of information about an author, including their given and family names, their place in the sequence of authors (i.e., first, additional, or last), and their affiliation. This is part of the output from a search on Crossref using habanero. E.g.:

        author_dict = {
            "given": "Jane",
            "family": "Doe",
            "sequence": "first",
            "affiliation": [],
        }

    Outputs
    -------
    name : string
        First name of the given author.
    """
    if "given" not in author_dict:
        name = ""
    else:
        # trim initials
        name = author_dict["given"].replace(".", " ").split()[0]
    return name


def names_from_xref(doi):
    """
    Get the first names of the first and last authors for a given DOI.

    Inputs
    ------
    doi : string
        The DOI of the paper whose first and last author names you want to know. Here, it's usually a citing paper.

    Outputs
    -------
    first_author : string
        The first name of the first author of the given paper.

    last_author : string
        The first name of the last author of the given paper.
    """
    cr = Crossref()
    title = ""
    works = cr.works(
        query=title, select=["DOI", "author"], limit=1, filter={"doi": doi}
    )
    first_author = ""
    last_author = ""
    if works["message"]["total-results"] > 0:
        item = works["message"]["items"][0]
        if "author" in item.keys():
            first_author = get_name_from_author_dict(item["author"][0])
            last_author = get_name_from_author_dict(item["author"][-1])
    return first_author, last_author


def name_to_gender(name, api_key=None, name_dict={}):
    f"""
    This function uses the gender-guesser pip package (https://pypi.org/project/gender-guesser/)
    and optionally the gender API (https://gender-api.com/) or a dictionary to guess the gender of
    the given name.

    Note that a major limitation of this code and the original paper is that this is a guess at the
    gender of a person based only on a first name, and it does not reflect the chosen gender of the
    author. Further, there are greater limitations if the name is not a traditionally western name.
    Last, the gender API has limitations in that it doesn't include all types of experienced genders.

    Inputs
    ------
    name : string
        The first name whose gender you want to guess.
    api_key : string
        The API key for the gender API. You can sign up for a free account and get an API key on
        the gender-api.com website. Optional.
    name_dict : dict
        Dictionary containing gender guesses and accuracy, the dictionary is used if the gender-guesser
        package returns 'unknown'. It is updated if a gender-api request is made.

    Outputs
    -------
    gender : string
        The guessed gender of the name.

    accuracy : int
        The accuracy of the gender guess, in percent.
    """
    # use the _gender_detector as a global variable to avoid re-generating it each time
    global _gender_detector

    # If the name is just an initial, return unknown
    if len(name) < 2:
        return "unknown", 0

    # create gender-guesser detcetor if it doesn't already exist
    if not "_gender_detector" in globals():
        _gender_detector = gender_detecor.Detector(case_sensitive=False)

    gender = _gender_detector.get_gender(name)
    accuracy = None
    if gender == "unknown":
        if name in name_dict.keys():
            gender = name_dict[name]["gender"]
            accuracy = name_dict[name]["accuracy"]
        elif api_key:
            url = f"https://gender-api.com/get?key={api_key}&name={name}"
            response = requests.get(url).json()
            gender = response["gender"]
            accuracy = response["accuracy"]
            name_dict[name] = {"gender": gender, "accuracy": accuracy}
            # save the updated names_dict
            with open(NAME_DICT_PATH, 'w') as name_dict_file:
                json.dump(name_dict, name_dict_file, indent=2)
        # if still unknown and there is a dash in the name, try on the first part of the name
        if gender == "unknown" and "-" in name:
            return name_to_gender(name.split("-")[0], api_key, dict)
    return gender, accuracy


def get_data(doi, df=None, api_key=None, name_dict={}):
    """
    For a given doi, get the names, genders, and gender accuracies of the first and last authors.

    Inputs
    ------
    doi: string
        The DOI of the paper whose authers' names and gender you want to get.
    df: pandas DataFrame
        DataFrame containing the data of already found DOIs, to avoid having to generate the
        data again. Optional.
    api_key: string
        The API key for the gender API. You can sign up for a free account and get an API key on
        the gender-api.com website. Optional.
    name_dict: dict
        Dictionary containing name gender data. Optional.

    Outputs
    -------
    data : dict or pandas.series
        dict or pandas.series with fields for first and last authors' names, guessed genders,
        and guess accuracies.
    """
    if df is not None and doi in df["doi"].values:
        data = df[df["doi"]==doi].iloc[0]
        data = data[["doi","first_author_name","first_author_gender","first_author_gender_accuracy",
                     "last_author_name","last_author_gender","last_author_gender_accuracy"]]
    else:
        fa_name, la_name = names_from_xref(doi)
        fa_gender, fa_accuracy = name_to_gender(fa_name, api_key, name_dict)
        la_gender, la_accuracy = name_to_gender(la_name, api_key, name_dict)
        data = {"doi": doi,
                    "first_author_name": fa_name, "first_author_gender": fa_gender,
                    "first_author_gender_accuracy": fa_accuracy,
                    "last_author_name": la_name, "last_author_gender": la_gender,
                    "last_author_gender_accuracy": la_accuracy}
    return data


if __name__ == "__main__":

    # Get path from working dir to src/data and join it to the relative paths
    path_to_src_data = os.path.dirname(sys.argv[0])
    for path_name in ["GENDER_API_KEY_PATH", "NAME_DICT_PATH", "DATAFILE_PATH"]:
        globals()[path_name] = os.path.join(path_to_src_data, globals()[path_name])

    # look for the gender_api_key and name_dict
    if os.path.isfile(GENDER_API_KEY_PATH):
        api_key = open(GENDER_API_KEY_PATH, "r").read().strip()
    else:
        api_key = None
        print(f"{GENDER_API_KEY_PATH} not found, gender-api won't be used.")

    if os.path.isfile(NAME_DICT_PATH):
        with open(NAME_DICT_PATH, 'r') as name_dict_file:
            name_dict = json.load(name_dict_file)
    else:
        name_dict = {}
        print(f"{NAME_DICT_PATH} not found, a new one will be created.")

    # look for the citing_paper.csv file
    if os.path.isfile(DATAFILE_PATH):
        old_papers = pd.read_csv(DATAFILE_PATH)
    else:
        old_papers = pd.DataFrame(columns=["doi"])
        print(f"{DATAFILE_PATH} not found, it will be generated from scratch.")

    # for each cited doi, get the citing dois and their name/gender data
    new_papers = pd.DataFrame(columns=["doi", "cited_entity"])
    for cited_entity, doi in CITED_DOIS.items():
        print("\n--------------\nLooking for citations of the ", cited_entity)
        citing_dois = get_dois(doi, citing=True)
        if not citing_dois:
            print("    No citations found :( \n")
        for n, citing_doi in enumerate(citing_dois):
            print("\tDOI %d / %d\r" % (n + 1, len(citing_dois)), end="")
            if not citing_doi in list(old_papers["doi"].values):
                new_row = get_data(citing_doi, new_papers, api_key, name_dict)
                new_row["cited_entity"] = cited_entity
                new_row["cited_doi"] = doi
                new_papers = new_papers.append(new_row, ignore_index=True)

    # for each citing doi, get the dois of the refs and their name/gender data
    print("\n--------------\nLooking in the referrences of the citing papers newly found.")
    citing_dois = new_papers.pivot(index="doi", columns="cited_entity", values="cited_entity")
    all_papers = old_papers.append(new_papers)
    for n, citing_doi_row in enumerate(citing_dois.itertuples()):
        print("\tDOI %d / %d                    \r" % (n + 1, len(citing_dois)), end="")
        ref_dois = get_dois(citing_doi_row.Index, citing=False)
        for k, ref_doi in enumerate(ref_dois):
            print("\tDOI %d / %d, reference %d / %d    \r" % (n + 1, len(citing_dois), k+1, len(ref_dois)), end="")
            if ref_doi not in CITED_DOIS.values():
                new_row = get_data(ref_doi, all_papers, api_key, name_dict)
                citing_entities = [entity for entity in CITED_DOIS.keys()
                                   if isinstance(getattr(citing_doi_row, entity, None), str)]
                new_row["citing_entity"] = " ".join(["paper citing cleanBib"]+citing_entities)
                new_row["citing_doi"] = citing_doi_row.Index
                all_papers = all_papers.append(new_row, ignore_index=True)

    # save the data as a .csv file
    print(f"\n\nSaving data to {DATAFILE_PATH}\n")
    all_papers.to_csv(DATAFILE_PATH)

    # save the potentially updated name_dict
    with open(NAME_DICT_PATH, 'w') as name_dict_file:
        json.dump(name_dict, name_dict_file, indent=2)
