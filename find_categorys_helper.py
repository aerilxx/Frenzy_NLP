#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 19:52:10 2019

@author: bingqingxie
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import bigrams,trigrams,ngrams
import ast 
from detail_helper import isMaterial
from find_brands_helper import list_duplicates_of, after_clean_text

#read txt dictioanry files
one_word_category_dict={}
with open('1_word_category.txt', 'r') as infile:
    one_word_category_dict = ast.literal_eval(infile.readline())

two_word_category_dict={}
with open('2_word_category.txt', 'r') as infile:
    two_word_category_dict = ast.literal_eval(infile.readline())
    
three_word_category_dict={}
with open('3_word_category.txt', 'r') as infile:
    three_word_category_dict = ast.literal_eval(infile.readline())

four_word_category_dict={}
with open('4_word_category.txt', 'r') as infile:
    four_word_category_dict = ast.literal_eval(infile.readline())


def find_category(text):
    words=word_tokenize(text)
    # a list of list by order combined category, original category, parent category
    cate_list = []     
    category_map = {}   
    bridge_map = {}
    
    fourgrams = ngrams(words,4)
    for w in list(fourgrams):
        pair = list(w)
        str1 = ' '.join(pair)

        if str1 in four_word_category_dict:
            print('4 word category: ')
            print(str1)
            text = text.replace(str1, str1.replace(' ',''))
            cate_list.append(str1.replace(' ',''))
            bridge_map[str1.replace(' ','')]=four_word_category_dict[str1]
            category_map[str1] = four_word_category_dict[str1]   

    words2 = word_tokenize(text)
    
    for w in list(nltk.trigrams(words2)):
        pair = list(w)
        str1 = ' '.join(pair)

        if str1 in three_word_category_dict:
            print('3 word category: ')
            print(str1)
            text = text.replace(str1, str1.replace(' ',''))
            cate_list.append(str1.replace(' ',''))
            bridge_map[str1.replace(' ','')]=three_word_category_dict[str1]
            category_map[str1] = three_word_category_dict[str1]   

    words3=word_tokenize(text)
    
    for w in list(nltk.bigrams(words3)):
        pair = list(w)
        str1 = ' '.join(pair)

        if str1.lower() in two_word_category_dict:
            print('2 word category: ')
            print(str1)
            text = text.replace(str1, str1.replace(' ',''))
            cate_list.append(str1.replace(' ',''))
            bridge_map[str1.replace(' ','')]=two_word_category_dict[str1]
            category_map[str1] = two_word_category_dict[str1]  

    words4=word_tokenize(text)

    for word in words4:
        if word in one_word_category_dict:
            print('1 word category:')
            print(word)
            cate_list.append(word)
            bridge_map[word]=one_word_category_dict[word]
            category_map[word] = one_word_category_dict[word]
    
        
    return text, cate_list, category_map, bridge_map


# construct map with key as index of the product and value of product
#text and categorys should be processed ->text2
def create_product_idx_map(text, categorys):
    category_idx_map = {}
    category_idx_map_2 = {}

    words = text.split(' ')
    for cat in categorys:
        if cat in words:
            idx=list_duplicates_of(words, cat)
            for id in idx:
                if cat is 'jean' or cat is'demin':
                    if isMaterial(text,id)==False:
                        print("False in create_product_idx_map")
                        category_idx_map[id] = cat
                else:
                    category_idx_map[id] = cat
                    
    # get index of category with 's
    words2 = word_tokenize(text)
    for cat in categorys:
        if cat in words2 and cat+"’s" in words:
            idx = words.index(cat+"’s")
            category_idx_map_2[idx] = cat
        elif cat in words2  and cat+"'s" in words:
            idx = words.index(cat+"'s")
            category_idx_map_2[idx] = cat
                
    category_idx_map.update(category_idx_map_2)
    
    return category_idx_map



