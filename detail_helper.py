#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:56:37 2019

@author: bingqingxie
"""

import nltk
from nltk.tokenize import word_tokenize
from operator import itemgetter
from calculate_score_helper import calculate_score, create_sentence_break
from find_brands_helper import list_duplicates_of
from collections import OrderedDict
from linked_map_class import convert_map_to_linkedlist

color_list = ['gold', 'purple', 'violet', 'brown', 'black', \
              'turquoise', 'green', 'yellow', 'fuchsia', 'pink', \
              'salmon', 'silver', 'blue', 'red', 'orange', 'gray', 'white', \
              'beige', 'ivory', 'mustard', 'navy', 'khaki', 'lavender']

pattern_list = ['print', 'printed', 'prints', 'pattern', 'patterned', 'graphic', \
                'emboss', 'embossed', 'cloqué', 'woven', 'weave', 'weaved', 'wicker', \
                'wickered', 'embroidery', 'embroidered', 'ditsy', 'exotic', 'mix', 'mixture', \
                'floral', 'logo', 'brand', 'branded', 'signature', 'designer name', 'paisley', \
                'plaid', 'checkered', 'check', 'flannel', 'polka dot', 'polkadot', 'dots', 'spot', 'spotted', \
                'circle', 'circles', 'geometric', 'quilt', 'quilted', 'quilting', 'tie dye', 'tie dyed', \
                'tropical', 'hawaiian', 'hawaii', 'tiger', 'lion', 'puma', 'cat', 'panther', 'leopard', 'cheetah', \
                'zebra', 'snake', 'snakeskin', 'python', 'croc', 'alligator', 'zig zag', 'zig-zag', 'zigzag', 'chevron', \
                'feather', 'feathers', 'tribal', 'houndstooth', 'lace', 'crochete', 'crocheted']

material_list = ['leather', 'fleece', 'linen', 'suede', 'lace', 'chiffon', 'wool', 'neoprene', 'cotton', 'tweed',
                 'corduroy', \
                 'velvet', 'satin', 'cashmere', 'synthetic', 'fur', 'canvas', \
                 'chambray', 'flannel', 'goose', 'tulle', 'denim', 'felt', 'wood', 'silk']



#logic: check if jeans or demin are material or product in text
def isMaterial(text, idx):
    words = word_tokenize(text)
    # words = text.split(' ')
    tags = nltk.pos_tag(words)
    keywords = ['is', 'are', 'were', 'will', 'would', 'with', 'I']

    for key in keywords:
        if key == tags[idx + 1][1]:
            return False
    if tags[idx][1] == 'NNS':
        return False
    # if fallowed by verb, must be product
    elif tags[idx + 1][1] == 'VBZ' or tags[idx + 1][1] == 'VBP' or tags[idx + 1][1] == 'VB':
        return False
    elif words[idx][0].isupper():
        return False

    return True


# if check is a verb or a pattern
def isPattern(text, idx):
    words = word_tokenize(text)
    # words = text.split(' ')
    tags = nltk.pos_tag(words)
    if tags[idx][1] == 'VBZ' or tags[idx][1] == 'VB' or tags[idx][1] == 'VBP':
        return False

    return True


# get index map by either pattern or color list
def find_idx_map_by_tokenize(text, list_type):
    idx_map = {}
    words = word_tokenize(text)
    # words = text.split(' ')
    for p in list_type:
        if p in words:
            idx = list_duplicates_of(words, p)
            for id in idx:
                idx_map[id] = p

    return idx_map


# get index map by either pattern or color list
def find_idx_map(text, list_type):
    idx_map = {}
    words = text.split(' ')

    for p in list_type:
        if p in words:
            idx = list_duplicates_of(words, p)
            for id in idx:
                idx_map[id] = p

    return idx_map


def convert_idx(map_tokenize, map_split, idx):
    i = 0
    order = OrderedDict()
    for key, values in map_split.items():
        order[key] = i
        i = i + 1

    j = 0

    ordert = OrderedDict()
    for key, values in map_tokenize.items():
        ordert[j] = key
        j = j + 1

    res = order[idx]
    return ordert[res]


def construct_map(text, list_type):
    map_tokenize = find_idx_map_by_tokenize(text, list_type)
    map_split = find_idx_map(text, list_type)
    final_idx_map = {}
    print(map_tokenize)
    print(map_split)
    # TODO: index is going out of range due to map_tokenize and split, take care into it.
    special_case_pattern = ['check', 'checked', 'print', 'printed']
    special_case_material = ['denim', 'jeans', 'jean']
    for key, value in map_split.items():
        if value in special_case_pattern:
            new_idx = convert_idx(map_tokenize, map_split, key)
            if isPattern(text, new_idx):
                final_idx_map[key] = value

        elif value in special_case_material:
            new_idx = convert_idx(map_tokenize, map_split, key)
            if isMaterial(text, new_idx):
                final_idx_map[key] = value

        else:
            final_idx_map[key] = value
    return final_idx_map
#
#
# def get_score(text, idx_category_map, idx_detail_map):
#     cidx = list(idx_category_map.keys())
#     didx = list(idx_detail_map.keys())
#     scorelist = []
#
#     for p in cidx:
#         for d in didx:
#             # logic : added the proximity distance, if distance is less then 150 then only we map them
#             if abs(p - d) <= 150:
#                 score = calculate_score(text, p, d)
#                 if score > 0.2:
#                     scorelist.append((idx_category_map[p], idx_detail_map[d], score))
#
#     return scorelist
#

def get_score_test2(text, idx_brand_map, idx_category_map, idx_detail_map, score_list):
    bidx = list(idx_brand_map.keys())
    cidx = list(idx_category_map.keys())
    didx = list(idx_detail_map.keys())

    stop_map, all_words = create_sentence_break(text)
    linked = convert_map_to_linkedlist(stop_map)

    max_score_for_each_cat = {}
    #logic : to find add the detils_category mapping
    for c in cidx:
        for d in didx:
            if abs(c - d) < 20:
                score = calculate_score(stop_map, linked, c, d, all_words)
                if d not in max_score_for_each_cat and score >= 0.1:
                    max_score_for_each_cat[d] = (c, score)
                elif d in max_score_for_each_cat and score > max_score_for_each_cat[d][1]:
                    max_score_for_each_cat[d] = (c, score)

    all_key_to_be_del = []

    #logic: trying to map each category in detail with closest possible brand
    for d in max_score_for_each_cat:
        c = max_score_for_each_cat[d][0]

        #logic: took default values just to compare and find max brand_idx before that category
        closest_brand = bidx[0]
        closest_dist = 1000

        for s in score_list:

            #logic: all brands having same category name
            if idx_category_map[s[1]] == idx_category_map[c]:
                if abs(c-s[0]) < closest_dist:
                    closest_brand = s[0]
                    closest_dist = abs(c - s[0])

        if closest_dist != 1000:
            c_idx, score = max_score_for_each_cat[d]
            max_score_for_each_cat[d] = (closest_brand, c_idx, score)
        else:
            all_key_to_be_del.append(d)
            
    # logic : deleting all the unnecessary brands
    for key in all_key_to_be_del:
        del max_score_for_each_cat[key]

    dic = {}
    #logic: finding all the score between brands and details, and cats and details
    for s in score_list:
        for b in bidx:
            for c in cidx:
                for d in didx:
                    if s[0] == b and s[1] == c:
                        # logic : added the proximity distance, if distance is less then 150 then only we map them

                        if abs(b-c)>250 or abs(c-d)>250 or abs(b-c)>250:
                            continue

                        score_brand_det = calculate_score(stop_map, linked, b, d, all_words)
                        score_cat_det = calculate_score(stop_map, linked, c, d, all_words)

                        score = (score_brand_det + score_cat_det) / 2.0
                        if d in dic :
                            prev_score = dic[d][2]
                            if score > prev_score:
                                dic[d] = (b, c, score)
                        elif d not in dic and score>0:
                            dic[d] = (b, c, score)

    return dic, max_score_for_each_cat

def get_highest_pair_by_category(scorelist, category):
    blist = []
    for s in scorelist:
        # set thread
        if s[0] == category and s[2] >= 0.25:
            blist.append(s)

    if blist == []:
        return []
    else:
        return max(blist, key=itemgetter(2))


def get_highest_pair_by_category_test(scorelist, category, brand):
    blist = []
    for s in scorelist:
        if s[0] == category and s[2] >= 0.25:
            blist.append(s)

    if blist == []:
        return []
    else:
        return max(blist, key=itemgetter(2))


def get_result_test2(text, idx_brand_map, idx_category_map, list_type, score_list):
    idx_detail_map = construct_map(text, list_type)
    det_scorelist, extra_details = get_score_test2(text, idx_brand_map, idx_category_map, idx_detail_map, score_list)
    return det_scorelist, idx_detail_map, extra_details
