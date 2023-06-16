#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 18:05:51 2021
@author: lunadana

C598 - HW8, Q1
"""

import pandas as pd 
import sys, os 
import json

def generate_count(input_path, f_stopwords):
    
    poney_keys = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    pony_dict = {}
    
    # Get the stop words
    with open(f_stopwords) as f:
        stopwords_list = list(f)
    stopwords_list = [x[:-1] for x in stopwords_list]
    
    # Open file as dataframe
    df_dialog = pd.read_csv(input_path)
    
    # Pony and dialog column to lower case
    df_dialog['pony']   = df_dialog['pony'].str.lower()
    df_dialog['dialog'] = df_dialog['dialog'].str.lower()
    
    # Only keep allowed ponies
    df_dialog = df_dialog[df_dialog['pony'].isin(poney_keys)]
    
    # Remove punctuation and non alphanumeric
    df_dialog['dialog'] = df_dialog['dialog'].str.replace('[^a-zA-Z0-9 ]', '',regex=True)
    
    # Get counts for each pony
    for pony in poney_keys:
        df_temp = df_dialog[df_dialog['pony'] == pony]
        list_of_all_words = ' '.join([i for i in df_temp['dialog']]).split()
        # create a dictionnary of words
        dict_words = {}
        for word in list_of_all_words:
            # if word is in stop word list then continue and discard it
            if word in stopwords_list:continue
            if word in dict_words : dict_words[word] = dict_words[word]+1
            else:dict_words[word] = 1 
        #Only keep words with more than 4 as count    
        dict_words = {key:val for key, val in dict_words.items() if val > 4}
        pony_dict[pony] = dict_words
    return pony_dict
    
def main():
    parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    f_stopwords = parent + "/data/stopwords.txt"
    
    f_clean_dialog = sys.argv[4]
    word_counts_json = sys.argv[2]
    content = generate_count(f_clean_dialog,f_stopwords)
    # Writing to output file
    json_object = json.dumps(content, indent = 4)
    with open(word_counts_json, "w") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":
    main()
    