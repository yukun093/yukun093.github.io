---
title: "Gene-expression-profile"
excerpt: "Tissue type classification based on microarray gene expression profiles<br/><img src='/images/DNA-Microarray.png'>"
permalink: /project/project-Gene-expression-profile/
dataset: https://drive.google.com/file/d/1hkkFh4T9PkP5L64gPTxjU6gg-TugRYcR/view?usp=sharing
codeurl: 'https://yukun093.github.io/files/project4-code.pdf'
collection: project
---

------

It is one project of machine learning with python from Aalto university, and the data set was one of the total dataset. The full dataset can be found at https://www.ebi.ac.uk/arrayexpress/, and part of that is subordinated to accession number E-MTAB-62([data_subset.csv](https://yukun093.github.io/files/data_subset.csv)). The first columns of 'data_subset.csv' file (file located in 'coursedata' folder) contains ID's of samples (e.g. 'GSM23227.CEL') and analyses info ('RMA') and the rest - expression values for 3000 genes. Here, based on expression profile of samples, the type of tissue should be predicted. Also multiple types of tissue which is subordinated to {'cell line', 'disease', 'neoplasm', 'normal'} should be mentioned as well.

## Introduction

"A microarray is a laboratory tool used to detect the expression of thousands of genes at the same time. DNA microarrays are microscope slides that are printed with thousands of tiny spots in defined positions, with each spot containing a known DNA sequence or gene." The microarray data for this problem consists of normalized relative expression of certain genes measured in different tissue. There are 3000 gene probes and 2000 samples. The full dataset can be found at https://www.ebi.ac.uk/arrayexpress/ (accession number E-MTAB-62). It should be noted that codes first are referred by teaching assistant of 2021-spring of course CS-EJ3211, since that would be better and much cleaner than mine.

## Result of binary classification

Additionally, here using f1_score to show the accuracy with matrix format.
$$
F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
$$
For example, here using training accuracy and testing accuracy to express the result with pipeline and using f1-score to check its reliability.

<div align=center><img src='/images/binary-classification.png'></div>

## Result of multiclass classification

For part II, the dataset is the multiclass classification which are 'cell line', 'disease', 'neoplasm', 'normal'. Here, data would not be removed due to its four-class classification. The f1-score is expressed across different gamma and C.

<div align=center><img src='/images/scores-for-test-set.png'></div>

Here the result is shown as one final evaluation.

<div align=center><img src='/images/final-evaluation.png'></div>

In the following link, the [code](https://drive.google.com/file/d/1hkkFh4T9PkP5L64gPTxjU6gg-TugRYcR/view?usp=sharing) could be checked.