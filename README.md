# GOST_Evaluation
This is the evaluation and analysis script for the Gene Ontology Semantic Tagger (GOST) used for our Biomedical Text Mining (BIoTM) Project.

This work involves applying the GOST to the an independently annotated corpus [CRAFT (Colorado Richly Annotated Full-Text)](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-13-161). CRAFT is a collection of 97 full-length, open-access biomedical journal articles that have been annotated both semantically and syntactically to serve as a research resource for the biomedical natural-language-processing (NLP) community.

The evaluation process is a preceeded by a set of pre-processing steps implemented in the `eval_gost_api.py` python script (included) and described below.

## Preparing the CRAFT data
This involves extracting the necessary annotated data from the original xml format (see the  which is then prepared and presented in plain text format for the  
