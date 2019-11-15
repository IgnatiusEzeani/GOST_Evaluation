# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 12:37:14 2019

@author: igeze
"""
import os, glob, subprocess
import xml.etree.ElementTree as ET
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

def read_tagged_files(folder, file_type='craft'):
    tag_dict = defaultdict(Counter)
    for f in os.listdir(folder):
        with open(f'{folder}/{f}', 'r', encoding='utf8') as f:
            for entry in f:
                details = entry.strip().split()
                tag_dict[details[0]].update([" ".join(details[1:])])
    return tag_dict

#def read_tagged_files(folder, file_type = 'gost'):
#    tag_dict = {}
#    for f in os.listdir(folder):
#        with open(f'{folder}/{f}', 'r', encoding='utf8') as f:
#            for entry in f:
#                details = entry.strip().split()
#                if not details[0] in tag_dict:
#                    tag_dict[details[0]] = details[1:]
#    return tag_dict

def evaluate(craft_dict, gost_dict, top=0):
    print(f"\n{'-'*10} Top {top} {'-'*10}")
    gold, pred = [],[]
    for go_id, words in craft_dict.items():
        gold.append(go_id)
        gost_go_ids = []
        if top and len(words)>1:
            for word in words:
                if word in gost_dict: gost_go_ids.append(gost_dict[word])
            if len(gost_go_ids)>1: 
                zipped = list(zip(gost_go_ids[0], gost_go_ids[1]))[:top]
            else: zipped = gost_go_ids
            if any(go_id in l for l in zipped):
                pred.append(go_id)
            else: pred.append('GO:0008150')
        else:
            for word in words:
                if word in gost_dict:
                    gost_go_ids.extend(gost_dict[word])
            if go_id in set(gost_go_ids): pred.append(go_id)
            else: pred.append('GO:0008150')
    return gold, pred

#def show_results(top):
#    golds, preds = evaluate(craft_dict, gost_dict, top)
#    print(f"{'Accuracy:':>10s} {accuracy_score(golds, preds)*100:.2f}%")
#    print(f"{'Precision:':>10s} {precision_score(golds, preds, average='micro')*100:.2f}%")
#    print(f"{'Recall:':>10s} {recall_score(golds, preds, average='micro')*100:.2f}%")
#    print(f"{'F1:':>10s} {f1_score(golds, preds, average='micro')*100:.2f}%")
#    

craft_xml = "craft_GO_BP_knowtator"
craft_tagged = "craft_tagged"
craft_untagged = "craft_untagged"
gost_tagged = "gost_tagged"

api_prefix = "curl -F type=rest -F email=hello -F tagset=c7 -F style=vert -F"
api_url = "http://ucrel-api.lancaster.ac.uk/cgi-bin/gost.pl"

#extract_xml(craft_xml, craft_tagged, craft_untagged)
#gost_tag_craft(api_prefix, api_url, gost_tagged)

craft_dict = read_tagged_files(craft_tagged)
#gost_dict = read_tagged_files(gost_tagged)

tops = [1, 5, 10, 0]

#for top in tops:
#    show_results(top)

# Top 10 most predicted GO_ids
#[('GO:0008150', 1041),
# ('GO:0009987', 362),
# ('GO:0044699', 334),
# ('GO:0008152', 260),
# ('GO:0032502', 203),
# ('GO:0071704', 162),
# ('GO:0044237', 149),
# ('GO:0051179', 137),
# ('GO:0044763', 133),
# ('GO:0044767', 116)]
# total count = 7997
# Unique GO_ids = 1167

#Good for the analysis!
#total
#Out[57]: dict_values([1])
#
#for GO, C in craft_dict.items():
#    total = sum(C.values())    
#    
#
#total
#Out[59]: 1
#
#total=0
#for GO, C in craft_dict.items():
#    total += sum(C.values())  
#    
#
#total
#Out[61]: 12962
#
#sum([sum(C.values()) for GO, C in craft_dict.items()])
#Out[62]: 12962