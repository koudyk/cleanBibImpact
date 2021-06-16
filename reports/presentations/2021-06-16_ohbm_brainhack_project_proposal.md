---
marp: true
theme: default
---

# cleanBibImpact
### Do papers with a Citation Diversity Statement have more diverse citations?

Kendra Oudyk & Isil Bilgin
2021-06-16
OHBM Brainhack Project Pitch

---
<!-- paginate: true -->

![](images/dworkin_title.png)

---
<!-- paginate: true -->

# Women are cited less than expected

![](images/dworkin_fig2_upper_right.png)
**WM** = **Woman** first author & **Man** last author

---
# Limitations in terminology
>"...the methods used for gender determination are limited to binary man and woman gender assignments. 
>
>This study design, therefore, is not well accommodated to intersex, transgender and/or nonbinary identities and incorrectly assumes that all authors can be placed into one of two categories. 
>
> Ideally, future work will be able to move beyond the gender binary"

\- Dworkin et al. (2020)

---

# Diversity statement template
> ... our references contain `A`% woman(first)/woman(last), `B`% man/woman, `C`% woman/man, `D`% man/man, and `E`% unknown categorization...


---
# cleanBib
github.com/dalejn/cleanBib

"Probabilistically assign gender and race proportions of first/last authors pairs in bibliography entries"

---

# cleanBibImpact
## Do papers with a Citation Diversity Statement have more diverse citations?

---

# Preliminary results

![](figures/relative_diversity__with_swarm__with_title.png)
**WM** = **Woman** first author & **Man** last author

<!-- ---
:tada::tada: Looks like papers with diversity statements have more diverse citations :tada::tada: -->



---
# Goals for the OHBM Brainhack
- [1. Manual inspection of citing papers' diversity statement](https://github.com/koudyk/cleanBibImpact/projects/4) (Ground truth for Goal 2)


---
# Goals for the OHBM Brainhack
- [1. Manual inspection of citing papers' diversity statement](https://github.com/koudyk/cleanBibImpact/projects/4) (Ground truth for Goal 2)
- [2. Assess whether citing papers have more diverse reference lists](https://github.com/koudyk/cleanBibImpact/projects/2)


---
# Goals for the OHBM Brainhack
- [1. Manual inspection of citing papers' diversity statement](https://github.com/koudyk/cleanBibImpact/projects/4) (Ground truth for Goal 2)
- [2. Assess whether citing papers have more diverse reference lists](https://github.com/koudyk/cleanBibImpact/projects/2)
- [3. Review our language around gender](https://github.com/koudyk/cleanBibImpact/projects/3)




---
# Good first issues

- [Manually collect citation diversity data from citing papers for 2021](https://github.com/koudyk/cleanBibImpact/issues/15) (part of Goal 1)

![](images/manual_data_2021.png)

---
# Good first issues
- [Update manually-collected citation diversity data from citing papers for 2020](https://github.com/koudyk/cleanBibImpact/issues/16) (part of Goal 1)

![](images/manual_data_2020.png)


---
# Good first-ish issues 
- [Find self-citations in manually-collected data](https://github.com/koudyk/cleanBibImpact/issues/17) (Goal 1) 
![](figures/relative_diversity__with_self_citation_swarm.png)


---
# For more-experienced hackers

- [Goal 2: Assess whether citing papers have more diverse reference lists](https://github.com/koudyk/cleanBibImpact/projects/2)
  - Automatically list citing papers
  - Get a paper's reference list
  - Guess author genders
- [DevOps](https://github.com/koudyk/cleanBibImpact/projects)
  - better modularizing our code
  - testing
  - continuous integration
  
  

---
# Skills
| Goal                          | Skills needed                                 |
|-------------------------------|-----------------------------------------------|
| 1. Manual inspection of <br />citing papers' diversity statement      |- Google Scholar, <br />- spreadsheets (pasting data), <br />- beginner Python (optional), <br />- Git 0-1 (optional) |
| 2. Assess whether citing papers <br />have more diverse reference lists   | - Confirmed-expert Python, <br />- working with APIs, <br />- Git 2, <br />- DevOps      |
| 3. Review language around gender |- Familiarity with gender theory, <br />- Git 0-1  (optional)             |



---
## chat with us on Mattermost 😊
![](images/mattermost_header.png)








