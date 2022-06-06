---
title: "Gene-expression-profile"
excerpt: "Tissue type classification based on microarray gene expression profiles<br/><img src='/images/DNA-Microarray.png'>"
permalink: /project/project-Gene-expression-profile/
dataset: 'yukun093.github.io/files/data_subset.csv'
collection: project
---

------

It is one project of machine learning with python from Aalto university, and the data set was one of the total dataset.

The full dataset can be found at https://www.ebi.ac.uk/arrayexpress/, and part of that is subordinated to accession number E-MTAB-62. The first columns of 'data_subset.csv' file (file located in 'coursedata' folder) contains ID's of samples (e.g. 'GSM23227.CEL') and analyses info ('RMA') and the rest - expression values for 3000 genes. Here, based on expression profile of samples, the type of tissue should be predicted. Also multiple types of tissue which is subordinated to {'cell line', 'disease', 'neoplasm', 'normal'} should be mentioned as well. 

## Introduction

"A microarray is a laboratory tool used to detect the expression of thousands of genes at the same time. DNA microarrays are microscope slides that are printed with thousands of tiny spots in defined positions, with each spot containing a known DNA sequence or gene."

The microarray data for this problem consists of normalized relative expression of certain genes measured in different tissue. There are 3000 gene probes and 2000 samples. The full dataset can be found at https://www.ebi.ac.uk/arrayexpress/ (accession number E-MTAB-62).

## Data cleaning

first, the data should be cleaned to remove the space, null, 