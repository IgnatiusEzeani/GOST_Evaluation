# GOST_Evaluation
This is the evaluation and analysis script for the Gene Ontology Semantic Tagger (GOST) used for our Biomedical Text Mining (BIoTM) Project.

This work involves applying the GOST to the an independently annotated corpus [CRAFT (Colorado Richly Annotated Full-Text)](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-13-161). CRAFT is a collection of 97 full-length, open-access biomedical journal articles that have been annotated both semantically and syntactically to serve as a research resource for the biomedical natural-language-processing (NLP) community.

The evaluation process is a preceeded by a set of pre-processing steps implemented in the `eval_gost_api.py` python script (included) and described below.

## Preparing the CRAFT data
This involves extracting the necessary annotated data from the original xml format (see one of the [craft_GO_BP_knowtator](https://github.com/IgnatiusEzeani/GOST_Evaluation/tree/master/BioTM_Project/craft_GO_BP_knowtator) files) which are then prepared and presented in plain text format (examples are in the [craft_tagged](https://github.com/IgnatiusEzeani/GOST_Evaluation/tree/master/BioTM_Project/craft_tagged) folder) for the actual evaluation process. Each  instance of the data contains a _gene ontology ID_ followed by a word of phrase `<GOXXXXXXX> <word|phrase>`. These are similar to the [craft_untagged](https://github.com/IgnatiusEzeani/GOST_Evaluation/tree/master/BioTM_Project/craft_untagged) files which differ only in their not having the gene ontology IDs

## Data statistics

## Calling the GOST API and Cleaning the tagging results
We made the GOST API call with the extracted annotated data in the `craft_untagged` folder. When the GOST API is called with a text input, it returns a set of possible tags (gene ontology IDs or semantic tags) for each of the tokens (words, digits and punctuations) in the text. Although, there are phrases (multi-words) among the biomedical terms that were included in the USAS semantic lexicon.

To properly evaluate GOST on the CRAFT, we removed all non-word output tokens as well as words for which the returned tags are not GO IDS.

## Evaluation Methods

## Evaluation Results
