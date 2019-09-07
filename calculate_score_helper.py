# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 13:28:58 2019

@author: bingqingxie
"""

from nltk.tokenize import sent_tokenize
import operator
from operator import itemgetter
from linked_map_class import find_new_start, find_new_end, convert_map_to_linkedlist


# helper function to calculate index of the end of sentence
def sum_fib(array, pos):
    s = 0

    for i in range(pos + 1):
        s += array[i]

    return s


# create a map each element contains the start and end index of a sentence
def create_sentence_break(text):
    listofsentence = []
    all_words = []
    text = ' '.join(text.split(' '))
    
    # fix the bug where 2 words are connected together by special character
    for s in sent_tokenize(text.replace(u'\xa0', u' ')):
        s_words = s.split(' ')
        listofsentence.append(len(s_words))
        all_words.extend(s_words)
    listofsentence[0] = listofsentence[0] - 1
    li = [0] + listofsentence

    fib_li = []
    for i in range(len(li)):
        fib_li.append(sum_fib(li, i))

    sent_map = {}

    for idx in range(len(fib_li) - 1):
        sent_map[fib_li[idx]] = fib_li[idx + 1]

    # for key, values in sent_map.items():
    #     sent_map[key] = values

    return sent_map, all_words


# calculate each brand_category pairing score based on index (clean text)
def calculate_score(stop_map, linked, b_idx, c_idx, all_words):
    score = 0

    for start, end in stop_map.items():

        # category in front of brand and in the same sentence
        if start < c_idx < b_idx <= end:
            score = (c_idx - start) / (b_idx - start - 1)
            flag_comma = 0
            flag_sep = 0
            # logic: checking if I have ','(comma) in between, if yes then divide score by 2
            # print(all_words[c_idx: b_idx + 1])
            for i in range(c_idx, b_idx):
         
                if all_words[i] == '/' or  all_words[i] == '|':
                    flag_sep = 1
                    break
                
                # logic: if sentence contains ',' between brand and category, score - 0.2
                if all_words[i] == ',':
                    flag_comma = 1
                    break
                
            if flag_sep == 1:
                score = score / 8

            elif flag_comma == 1:
                score = score - 0.2

        # brand in front of category and in the same sentence
        elif start < b_idx < c_idx <= end:

            if end == b_idx + 1:
                score = (end - c_idx) / (end - b_idx)
            else:
                score = (end - c_idx) / (end - b_idx - 1)
            flag_comma = 0
            flag_sep = 0
      
            for i in range(b_idx, c_idx):
                # seperator logic: if there is / | in sentence, devide score by 4
                if all_words[i] == '/' or  all_words[i] == '|':
                    flag_sep = 1
                    break
                if all_words[i] == ',':
                    flag_comma = 1
                    break
                
            if flag_sep == 1:
                score = score / 8

            elif flag_comma == 1:
                score = score - 0.2

        # category in front of brand and in different sentence
        elif (start < b_idx < end) and c_idx < start:
            new_start = find_new_start(linked, start, end, c_idx)
            score = ((c_idx - new_start) / (b_idx - new_start - 1)) / 4

        # brand in front of category and in different sentence
        elif (start < b_idx < end) and c_idx > end:
            new_end = find_new_end(linked, start, end, c_idx)
            score = ((new_end - c_idx) / (new_end - b_idx - 1)) / 4

    return score


def get_pair_score_map(clean_text, brands, categorys, brand_map, product_map):
    brands_idx_array = list(brand_map.keys())
    category_idx_array = list(product_map.keys())

    stop_map, all_words = create_sentence_break(clean_text)
    linked = convert_map_to_linkedlist(stop_map)

    scorelist = []
    for b in brands_idx_array:
        for c in category_idx_array:
            # logic : used to limit the distance between brand and category to 250 only.
            if abs(b - c) <= 250:
                scorelist.append((b, c, calculate_score(stop_map, linked, b, c, all_words)))
    scorelist.sort(key=operator.itemgetter(2), reverse=True)

    return scorelist


def get_highest_score_pair_by_brand(scorelist, brand, brand_map):
    blist = []
    # logic: store all the scores below threshold in empty list, if and only if (blist) is empty then we return value from (empty) list
    empty = []
    max_list = []
    for s in scorelist:
        if brand_map[s[0]] == brand:
            if s[2] >= 0.1:
                    # logic: checking if score > 0.9, if its 1 then we append them all and send entire list, beacuse returning just the max value would return 1st occurance of 1.0

                    if s[2] >= 0.9:
                        max_list.append(s)
                    else:
                        blist.append(s)
            else:
                empty.append(s)

    if len(max_list) > 0:
        return max_list
    if blist == [] and empty == []:
        return []
    elif blist == [] and len(empty) > 0:
        return [max(empty, key=itemgetter(2))]
    else:
        blist = sorted(blist, key=itemgetter(2), reverse=True)
        max_val = blist[0][2]
        rlist= []
        while len(blist)> 0 and blist[0][2] >= (max_val - 0.2):
            rlist.append(blist.pop(0))
        return rlist


def get_highest_score_pair_by_category(scorelist, category, product_map):
    blist = []
    for s in scorelist:
        if product_map[s[1]] == category and s[2] >= 0.3:
            blist.append(s)

    if blist == []:
        return []
    else:
        return [max(blist, key=itemgetter(2))]


# get biggest socre combo based on category
def get_final_result(text, brands, categorys, brand_map, product_map):
    final = set()
    # logic : remove below
    scores = get_pair_score_map(text, brands, categorys, brand_map, product_map)
    # print(scores)
    for b in brands:
        b_score = get_highest_score_pair_by_brand(scores, b, brand_map)
        if b_score == []:
            pass
        else:
            for b in b_score:
                final.add((b))

    for c in categorys:
        c_score = get_highest_score_pair_by_category(scores, c, product_map)
        if c_score == []:
            pass
        else:
            for c in c_score:
                final.add((c))
    return sorted(final)





