# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 12:37:14 2019

@author: igeze
"""
import os, glob, subprocess
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from collections import Counter, defaultdict

def extract_xml(xml_tagged_dir, craft_tagged_dir, craft_untagged_dir):
    if not os.path.exists(craft_tagged_dir):
        print(f'Creating {craft_tagged_dir} ...')
        os.makedirs(craft_tagged_dir)
        if not os.path.exists(craft_untagged_dir):
            print(f'Creating {craft_untagged_dir} ...')
            os.makedirs(craft_untagged_dir)
        else:
            print(f'{craft_untagged_dir} already exists! Extraction aborted')
            return
    else:
        print(f'{craft_tagged_dir} already exists! Extraction aborted')
        return
    for f in glob.glob(f"{craft_xml}/*.xml"):
        root = ET.parse(f).getroot()
        #extract text with gene ontology tags
        with open(f"{craft_tagged_dir}/{f[22:-3]}tagged", 'w', encoding="utf8") as tagged_data:
            for class_mention in root.findall('classMention/mentionClass'):
                tagged_data.write(f"{class_mention.get('id')}\t{class_mention.text}\n")

        #extract text without gene ontology tags        
        with open(f"{craft_untagged_dir}/{f[22:-3]}untagged", 'w', encoding="utf8") as untagged_data:
            for class_mention in root.findall('classMention/mentionClass'):
                untagged_data.write(f"{class_mention.text}\n")

def clean_api_result(result):
    result_dict={}
    result = str(result).split("\\n")[3:-3]
    for res in result:
        word,_,_,ranked_tags,_ = res.split("\\t")
        taglist = [tag.split(".",1)[0] for tag in ranked_tags.split()]
        if word not in result_dict and taglist[0].startswith('GO'):
            result_dict[word] = taglist
    return result_dict

def gost_tag_craft(api_prefix, api_url, gost_tagged_dir):
    if not os.path.exists(gost_tagged_dir):
        print(f'Creating {gost_tagged_dir} ...')
        os.makedirs(gost_tagged_dir)
    result=""
    for i, f in enumerate(glob.glob("craft_untagged\*")):
        print(f'{i:2d}\t{f}')
        command = f"{api_prefix} text=@{f} {api_url}"
        with open(f'{gost_tagged_dir}/'+f.split("\\")[1][:-8]+'gost_tagged',
                  'w', encoding="utf8") as gost_file:
            result = clean_api_result(subprocess.check_output(command))
            for word in result:
                gost_file.write(f'{word}\t{" ".join(result[word])}\n')

def read_tagged_files(folder, file_type='gost'):
    if file_type=='craft':
        tag_dict = defaultdict(Counter)
        for f in os.listdir(folder):
            with open(f'{folder}/{f}', 'r', encoding='utf8') as f:
                for entry in f:
                    details = entry.strip().split()
                    tag_dict[details[0]].update([" ".join(details[1:])])
    else:
        tag_dict = {}
        for f in os.listdir(folder):
            with open(f'{folder}/{f}', 'r', encoding='utf8') as f:
                for entry in f:
                    details = entry.strip().split()
                    if not details[0] in tag_dict:
                        tag_dict[details[0]] = details[1:]
    return tag_dict

def evaluate(craft_dict, gost_dict, top=0, default_goid = 'GO:0010467', no_default=False):
#    print(f"\nbegin:{'-'*5} Top {top if top else 'All' } {'-'*5}")
    gold, pred, errors = [],[], []
    for go_id, concepts in craft_dict.items():
        gost_go_ids = []
        if top:
            for phrase, count in concepts.items():
                gold.extend([go_id]*count)
                
                for word in phrase.split():
                    if word in gost_dict: gost_go_ids.append(gost_dict[word])
                
                if len(gost_go_ids)>1: zipped = list(zip(gost_go_ids[0], gost_go_ids[1]))[:top]
                else: zipped = gost_go_ids
                
                if default_goid == 'GO:0000000': default_goid=zipped[0][0]
                    
                if any(go_id in l for l in zipped):
                    pred.extend([go_id]*count)
                else:
                    pred.extend([default_goid]*count)
                    if go_id!=default_goid:
                        errors.append((phrase, go_id, default_goid, count))
        else:
            for phrase, count in concepts.items():
                gold.extend([go_id]*count)
                for word in phrase.split():
                    if word in gost_dict:
                        gost_go_ids.extend(gost_dict[word])
                if default_goid == 'GO:0000000': default_goid=gost_go_ids[0][0]
                if go_id in set(gost_go_ids): pred.extend([go_id]*count)
                else:
                    pred.extend([default_goid]*count)
                    if go_id!=default_goid:
                        errors.append((phrase, go_id, default_goid, count))
#    print(f"end:{'-'*5} Top {top if top else 'All' } {'-'*5}")
    return gold, pred, errors

def show_stats(craft_dict):
    # Finish this later
    pass

def show_results(top, dg):
    golds, preds, errors = evaluate(craft_dict, gost_dict, top, default_goid=dg)
#    total = sum([(g!=p)*c for _,g,p,c in errors])
#    print(len(golds), len(preds), total, len(golds)-total/len(golds))
    print(f"Top {str(top) if top else 'All':3s} & {accuracy_score(golds, preds)*100:.2f}", end=' & ')
    print(f"{precision_score(golds, preds, average='macro')*100:.2f}", end=' & ')
    print(f"{recall_score(golds, preds,  average='macro')*100:.2f}", end=' & ')    
    print(f"{f1_score(golds, preds, average='macro')*100:.2f}\\")
    return errors

craft_xml = "craft_GO_BP_knowtator"
craft_tagged = "craft_tagged"
craft_untagged = "craft_untagged"
gost_tagged = "gost_tagged"

api_prefix = "curl -F type=rest -F email=hello -F tagset=c7 -F style=vert -F"
api_url = "http://ucrel-api.lancaster.ac.uk/cgi-bin/gost.pl"

#extract_xml(craft_xml, craft_tagged, craft_untagged)
#gost_tag_craft(api_prefix, api_url, gost_tagged)

craft_dict = read_tagged_files(craft_tagged, 'craft')
gost_dict = read_tagged_files(gost_tagged)

default_goids = [
        ('GO:0000000', 'first goid'),
        ('GO:0008150', 'most gost'),
        ('GO:0010467','most craft')
        ]

tops = [1, 5, 10, 15, 0]

for dg, desc in default_goids:
    print(f"{'='*5} {dg}_{desc} {'='*5}")
    
    error_dict={}
    for top in tops:
        error_dict[top] = show_results(top, dg)
    
"""
\hline
GO:0000000_first goid
\hline
\textit{Top 1} & 51.54 & 12.40 & 12.48 & 12.42 \\
\textit{Top 5} & 62.03 & 30.85 & 30.93 & 30.87 \\
\textit{Top 10} & 67.84 & 40.43 & 40.50 & 40.45 \\
\textit{Top 15} & 68.73 & 42.65 & 42.72 & 42.67 \\
\textit{Top ALL} & 81.04 & 61.80 & 61.86 & 61.82 \\
\hline

c.most_common(10)
[('GO:0008150', 1041),
 ('GO:0009987', 362),
 ('GO:0044699', 334),
 ('GO:0008152', 260),
 ('GO:0032502', 203),
 ('GO:0071704', 162),
 ('GO:0044237', 149),
 ('GO:0051179', 137),
 ('GO:0044763', 133),
 ('GO:0044767', 116),
 ('GO:0065007', 114),
 ('GO:0048856', 97),
 ('GO:0051234', 92),
 ('GO:0006807', 86),
 ('GO:0050789', 85),
 ('GO:0044238', 83),
 ('GO:0032501', 79),
 ('GO:0071840', 78),
 ('GO:0043170', 76),
 ('GO:0016043', 76)]
"""