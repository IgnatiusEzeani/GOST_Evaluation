# GOST_Evaluation
This is the evaluation and analysis script for the Gene Ontology Semantic Tagger (GOST) used for our Biomedical Text Mining (BioTM) Project.

This work involves applying the GOST to the an independently annotated corpus [CRAFT (Colorado Richly Annotated Full-Text)](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-13-161). CRAFT is a collection of 97 full-length, open-access biomedical journal articles that have been annotated both semantically and syntactically to serve as a research resource for the biomedical natural-language-processing (NLP) community.

The evaluation process is a preceeded by a set of pre-processing steps implemented in the `eval_gost_api.py` python script (included) and described below.

## Preparing the CRAFT data
This involves extracting the necessary annotated data from the original xml format (see one of the [craft_GO_BP_knowtator](https://github.com/IgnatiusEzeani/GOST_Evaluation/tree/master/BioTM_Project/craft_GO_BP_knowtator) files) which are then prepared and presented in plain text format (examples are in the [craft_tagged](https://github.com/IgnatiusEzeani/GOST_Evaluation/tree/master/BioTM_Project/craft_tagged) folder) for the actual evaluation process. Each  instance of the data contains a _gene ontology ID_ followed by a word or phrase e.g.:

- `<GO:XXXXXXX> <word|phrase>`
  
These are similar to the [craft_untagged](https://github.com/IgnatiusEzeani/GOST_Evaluation/tree/master/BioTM_Project/craft_untagged) files which differ only in their not having the gene ontology IDs

## CRAFT Data statistics and analysis

| Test1 |Test2|
| ------------- |:--------:|
| No of files   | 97       |
| No of entries | 12,262   |
| Unique `GO ids`| 721     |


## Calling the GOST API and Cleaning the tagging results
We made the GOST API call with the extracted annotated data in the `craft_untagged` folder. When the GOST API is called with a text input, it returns a set of possible tags (gene ontology IDs or semantic tags) for each of the tokens (words, digits and punctuations) in the text. Although, there are phrases (multi-words) among the biomedical terms that were included in the USAS semantic lexicon.

To properly evaluate GOST on the CRAFT, we removed all non-word output tokens as well as words for which the returned tags are not `GO ID`s.

## Evaluation Methods
**I need suggestions here!!!**: At the moment the evaluation method passes each instance from the extracted untagged gold dataset ([craft_untagged](https://github.com/IgnatiusEzeani/GOST_Evaluation/tree/master/BioTM_Project/craft_untagged)) and compares the returned output with the expected output in the tagged version ([craft_tagged](https://github.com/IgnatiusEzeani/GOST_Evaluation/tree/master/BioTM_Project/craft_tagged)).

However, remember that GOST will return a set of `GO id`s for each word (non-words or words without `GO id` tags are excluded) of the text given. For example, if we pass `brain` to GOST we will get something like:

```
brain	GO:0048856 GO:0048513 GO:0032502 GO:0007420 GO:0032502 GO:0044767 GO:0008150 GO:0008150 GO:0044699
```
These `GO id`s are ranked according their likelihood (based on `GOST`) and so `GO:0048856` is assumed to be the most likely. So, for evaluation purpose, we implement different schemes:

- `Top 1`: If the first `GO id` is the correct one based on the CRAFT dataset. This is the most strict.
- `Top 5`: If the correct `GO id` is among the top 5 predicted by GOST
- `Top 10`: If the correct `GO id` is among the top 10 predicted by GOST
- `Top ALL`: If the correct `GO id` is in the list of all ids predicted by GOST

Also, if we pass `brain development` instead, GOST may return:  

```
brain	GO:0048856 GO:0048513 GO:0032502 GO:0007420 GO:0032502 GO:0044767 GO:0008150 GO:0008150 GO:0044699
development	GO:0048856 GO:0048513 GO:0032502 GO:0007420
```
Here we have a similar evaluation method but the `GO id`s in the similar positions for each word are grouped together before applying the schemes. For example, we will pre-process the result so that `brain development` result will look like:
```
brain development (GO:0048856, GO:0048856) (GO:0048513, GO:0048513) (GO:0032502, GO:0032502) ... 
```
Then we can apply the schemes by checking whether the CRAFT representation of `brain development` is found in the 1st tuple or within the first 5 or 10 tuples etc.

## Evaluation Results
**I will put the results in a nicer table later...I promise ;)** Below is the result that I have got so far:

```
---------- Top 1 ----------
 Accuracy: 12.21%
Precision: 12.21%
   Recall: 12.21%
       F1: 12.21%

---------- Top 5 ----------
 Accuracy: 30.65%
Precision: 30.65%
   Recall: 30.65%
       F1: 30.65%

---------- Top 10 ----------
 Accuracy: 41.19%
Precision: 41.19%
   Recall: 41.19%
       F1: 41.19%

---------- Top ALL ---------
 Accuracy: 62.83%
Precision: 62.83%
   Recall: 62.83%
       F1: 62.83%
```

This code is being cleaned-up because I have spotted some minor issues that may likely affect the results in some way e.g.
 
 - the code conflate all occurences of a specific `GO id`s into one in the dictionary that it builds from reading the dataset
 - Also, although we may not be using all the metrics,  I am yet unsure why I am getting the same values for all the metrics
 
## Other Issues (from meeting with Paul)
**Again, I need suggestions here!!!**: A question that came up was: _Shouldn't we be tagging the running text of articles instead?_.

Yes, we could do that as well but it is not clear to me how we intend to evaluate the output against the CRAFT dataset. Personally a
I guess we did this because we wanted to directly compare the GOST output with the pre-extracted CRAFT dataset entries.

Anyway, something may strike me in the morning but for now, I need ideas please..
