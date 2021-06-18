# cleanBibImpact

## Vision
Gender imbalance is a big problem in academic research, and it is even reflected in our citation behavior. Our goal is to assess the 'impact' of the [cleanBib](https://github.com/dalejn/cleanBib) tool, which was created to make researchers more aware of this problem. This tool can be used to assess the gender balance of authors in a reference list. Specifically, we want to find papers that cite the cleanBib [code](https://doi.org/10.5281/zenodo.3672109)/[paper](https://doi.org/10.1038/s41593-020-0658-y)/[preprint](https://doi.org/10.1101/2020.01.03.894378), and see whether those citing papers have better gender balance in their reference lists than papers that do not.

The cleanBib project and the associated paper are fairly new, so there aren't many papers that cite it yet. This project was started at the [2020 OHBM Brainhack Hackathon](https://ohbm.github.io/hackathon2020/), and we hope to continue it at future [Brainhacks](https://brainhack.org/) when more papers have used cleanBib.

## A note on 'gender'
Unfortunately, we're making some poor assumptions in our use of 'gender' in this project. We use both the [gender-guesser](https://pypi.org/project/gender-guesser/) package and the [Gender API](https://gender-api.com/) to guess the gender of a person based on their first name. Some of our limitations include:
- The gender guesses made by the tool may not reflect the experienced gender of the individual,
- This tool is biased in that it's better at recognizing 'western' names, and
- This tool has only 3 gender categories ("female", "male", and "unknown"), and so it does not reflect the full experienced gender spectrum.

Despite these limitations, we believe this project is worthwhile for assessing and encouraging gender equity in research. Please let us know you have ideas for how we could overcome these limitations or related problems that you spot! To do so, please comment on this [issue](https://github.com/koudyk/cleanBibImpact/issues/7) or open a new one.

## Milestones
This is a work in progress. Here are some steps we'll need to complete to reach our goal:
- [x] **0. Manual inspection of citing papers' diversity statement**. As a first step, we're doing some manual data collection and visualization. We manually searched for papers that cite the code, paper, and/or preprint associated with cleanBib, and then compared their citations' gender diversity to the benchmarks reported in the [paper](https://doi.org/10.1038/s41593-020-0658-y). *You can see our results in this [notebook](https://github.com/koudyk/cleanBibImpact/blob/master/src/visualization/visualize_manual_data.ipynb) as of January 2021.
- [ ] **1. List citing papers**. Automatically list papers that cite the code, paper, and/or preprint associated with cleanBib. *We're currently at a stage where we can do this and we can get the gender guesses for the citing papers' first and last authors, but not for the citing papers' references. All this is currently done in this [script](https://github.com/koudyk/cleanBibImpact/blob/master/src/data/make_dataset.py).*
- [ ] **2. List citing papers' citations**.
- [ ] **3. Guess genders** of the first and last authors of the  citing papers' citations using the [Gender API](https://gender-api.com)
- [ ] **4. Group citations** into one of the following classes, using the gender guesses from the previous step:
  - Man & Man (i.e., man first author & man last author)
  - Woman & Man
  - Man & Woman
  - Woman & Woman
- [ ] **5. Compare class distributions**. Compare the numbers of papers in each class for a) papers that cite the cleanBib code/paper/preprint, versus b) papers that do not. For the papers that do not, we could either use the numbers reported in the paper, or gather similar papers that do not cite the cleanBib code/paper/preprint and run a causal analysis.

## Contributing
We welcome collaborators! 🤗
If you're interested, please see our [Contributing](https://github.com/koudyk/cleanBibImpact/blob/master/CONTRIBUTING.md) guidelines and our [Code of Conduct](https://github.com/koudyk/cleanBibImpact/blob/master/CODE_OF_CONDUCT.md).


## Installation
*Note that this project is very much in development, so the requirements.txt file may not be up do date, and we haven't finished the setup.py file yet.*

1. Get to project directory: `cd /path/to/repo`
2. Create a virtual python environment: `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`
4. Install the requirements: `pip install -r requirements.txt`

To use the code that interacts with the [Gender API](https://gender-api.com/), you need to sign up for a free account and get an API key, then save it in a file called `src/data/gender_api_key.txt`.
