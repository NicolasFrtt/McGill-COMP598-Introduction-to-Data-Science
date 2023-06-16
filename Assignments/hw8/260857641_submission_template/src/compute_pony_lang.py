#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 18:05:51 2021
@author: lunadana

C598 - HW8, Q2
"""

import pandas as pd 
import sys, os 
import json
import math
        
def generate_tfidf(word_counts_json, n):
    
    with open(word_counts_json,"r") as file:
        word_count_dict = json.load(file)
    
    poney_keys = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    n_ponies = len(poney_keys)    
    
    def tf(w, pony):
        try : return word_count_dict[pony][w]
        except : return 0
    
    def idf(w):
        n_pony_w = 0
        for dic in word_count_dict.keys():
            if w in word_count_dict[dic]:
               n_pony_w = n_pony_w +1  
        return math.log(n_ponies/n_pony_w)
    
    def tf_idf(w, pony):
        return tf(w, pony)*idf(w)
    
    dict_tf_idf = {}
    for pony in poney_keys:
        dict_temp_words = {}
        for w in word_count_dict[pony]:
            dict_temp_words[w] = tf_idf(w, pony)
        dict_temp_words = sorted(dict_temp_words.values(), reverse=True)
        dict_tf_idf[pony] = dict_temp_words[0:n]
    return dict_tf_idf

def main():
    pony_counts_json = sys.argv[2]
    n = int(sys.argv[4])
    content = generate_tfidf(pony_counts_json, n)
     # Writing to output file
    json_object = json.dumps(content, indent = 4)
    print(json_object)
        
if __name__ == "__main__":
    main()
