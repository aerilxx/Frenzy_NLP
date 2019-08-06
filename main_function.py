#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 17:33:11 2019

@author: bingqingxie
"""

from find_brands_helper import find_all_brands, create_brand_idx_map
from find_categorys_helper import find_category, create_product_idx_map
from calculate_score_helper import get_final_result
from detail_helper import get_result_test2
from blog_crawler import crawl_text
import json
import time
import sys

material_dict = {'canvas': 'canvas', 'cashmere': 'cashmere', 'chiffon': 'chiffon', 'corduroy': 'corduroy',
                 'jersey': 'cotton',
                 'supimacotton': 'cotton', 'knit': 'cotton', 'denim': 'denim', 
                 'felted': 'felt',
                 'felt': 'felt', 'plaid': 'flannel', 'flannel': 'flannel', 'fleece': 'fleece', 'chambray': 'chambray',
                 'camel hair': 'fur', 'calfhair': 'fur', 'camelhair': 'fur', 'shearlig': 'fur', 'cotton': 'cotton',
                 'goose': 'goose', 'lacey': 'lace', 'lace': 'lace', 'calfskin': 'leather', 'lambskin': 'leather',
                 'goat': 'leather',
                 'cowhide': 'leather', 'calf': 'leather', 'lamb': 'leather', 'goatskin': 'leather',
                 'kangaroo': 'leather', 'snakeskin': 'leather',
                 'python': 'leather', 'snake': 'leather', 'ostrich': 'leather', 'alligator': 'leather',
                 'gator': 'leather', 'croc': 'leather',
                 'crocodile': 'leather', 'linen': 'linen', 'neoprene': 'neoprene', 'rubber': 'neoprene',
                 'satin': 'satin', 'silk': 'silk',
                 'nubuck': 'suede', 'suede': 'suede', 'rayon': 'synthetic', 'synthetic': 'synthetic',
                 'spandex': 'synthetic', 'viscose': 'synthetic',
                 'polyester': 'synthetic', 'elastane': 'synthetic', 'lycra': 'synthetic', 'nylon': 'synthetic',
                 'acrylic': 'synthetic', 'acetate': 'synthetic',
                 'polyurethane': 'synthetic', 'poly': 'synthetic', 'manmade': 'synthetic', 'man-made': 'synthetic',
                 'plastic': 'synthetic',
                 'modal': 'synthetic', 'eva': 'synthetic', 'foam': 'synthetic', 'velcro': 'synthetic',
                 'lurex': 'synthetic',
                 'tulled': 'tulle', 'tulle': 'tulle', 'tweed': 'tweed', 'velvet': 'velvet', 'wool': 'wool',
                 'wooden': 'wood'
                 }

pattern_dict = {'print': 'print', 'printed': 'print', 'prints': 'print', 'pattern': 'print', 'patterned': 'print',
                'graphic': 'print', \
                'emboss': 'emboss', 'embossed': 'emboss', 'cloqué': 'emboss', 'woven': 'woven', 'weave': 'woven',
                'weaved': 'woven', \
                'wicker': 'woven', 'wickered': 'woven', 'embroidery': 'woven', 'embroidered': 'woven', 'ditsy': 'ditsy',
                'exotic': 'exotic', \
                'mix': 'exotic', 'mixture': 'exotic', 'floral': 'floral', 'logo': 'logo', 'brand': 'logo',
                'branded': 'logo', 'signature': 'logo',
                'paisley': 'paisley', 'plaid': 'plaid', 'checkered': 'plaid', 'check': 'plaid', 'flannel': 'plaid',
                'polka dot': 'polka dot', 'polkadot': 'polka dot', 'dots': 'polka dot', 'spot': 'polka dot',
                'spotted': 'polka dot',
                'circle': 'circle', 'circles': 'circle', 'geometric': 'circle', 'quilt': 'quilt', 'quilted': 'quilt',
                'quilting': 'quilt', \
                'tie dye': 'tie dye', 'tie dyed': 'tie dye', 'tropical': 'tropical', 'hawaiian': 'tropical',
                'hawaii': 'tropical', \
                'tiger': 'leopard', 'lion': 'leopard', 'panther': 'leopard', 'leopard': 'leopard', 'cheetah': 'leopard',
                'zebra': 'zebra', \
                'snake': 'snake', 'snakeskin': 'snake', 'python': 'snake', 'croc': 'snake', 'alligator': 'snake',
                'zig zag': 'zigzag', \
                'zig-zag': 'zigzag', 'zigzag': 'zigzag', 'chevron': 'zigzag', 'feather': 'feather',
                'feathers': 'feather', 'tribal': 'tribal', \
                'lace': 'lace', 'crochete': 'lace', 'crocheted': 'lace','crochet': 'lace'}

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


# get detail id of color pattern material in db
def get_detail_id(word):
    material_id_map = {'canvas': 1, 'cashmere': 2, 'chiffon': 3, 'corduroy': 4, 'cotton': 5, 'denim': 6, 'felt': 7,
                       'flannel': 8, 'fleece': 9, 'fur': 10, 'goose': 11, 'lace': 12, 'leather': 13, 'linen': 14,
                       'neoprene': 15, 'rubber': 16, 'satin': 17, 'silk': 18, 'suede': 19, 'synthetic': 20, 'tulle': 21,
                       'tweed': 22, 'velvet': 23, 'wool': 24, 'wood': 25}
    color_id_map = {'brown': 1, 'gold': 2, 'yellow': 3, 'orange': 4, 'purple': 5, 'red': 6, 'pink': 7, 'black': 8,
                    'green': 9, 'blue': 10, 'turquoise': 11, 'white': 12, 'grey': 13, 'beige': 14, 'silver': 15,
                    'multicolor': 16, 'light blue': 17}
    pattern_id_map = {'print': 1, 'emboss': 2, 'woven': 3, 'ditsy': 4, 'exotic': 5, 'floral': 6, 'logo': 7,
                      'paisley': 8, 'plaid': 9, 'polka': 10, 'circle': 11, 'quilt': 12, 'tiedye': 13, 'tropical': 14,
                      'leopard': 15, 'zebra': 16, 'snake': 17, 'zigzag': 18, 'feather': 19, 'tribal': 20,
                      'houndstooth': 21, 'lace': 22}

    if word in material_id_map.keys():
        return material_id_map[word]

    if word in color_id_map.keys():
        return color_id_map[word]

    if word in pattern_id_map:
        return pattern_id_map[word]

    return None


def run_nlp_analysis(text):
    start = time.time()
    text = text.replace('’',"'")
    brands, text_with_clean_brand, brand_bridge_map = find_all_brands(text)

    # logic to replace all '.' with ' .'
    text_with_clean_brand = text_with_clean_brand.replace('.', ' . ')
    text_with_clean_catandbrand, categorys, category_map, cat_bridge_map = find_category(text_with_clean_brand)

    # logic : trying to remove the double spaces
    res = []
    for word in list(text_with_clean_catandbrand.split(' ')):
        if len(word) > 0:
            res.append(word)

    text_with_clean_catandbrand = ' '.join(res)
    # logic end

    idx_brand_map = create_brand_idx_map(text_with_clean_catandbrand, brands)
    idx_category_map = create_product_idx_map(text_with_clean_catandbrand, categorys)
    # print("idx brand map")
    # print(sorted(idx_brand_map.items()))
    # print("idx cat map")
    # print(sorted(idx_category_map.items()))
    score_list = get_final_result(text_with_clean_catandbrand, brands, categorys, idx_brand_map, idx_category_map)
    #print(score_list)
    end1 = time.time()
    print("Total time till getting score_list = ", end1 - start)
    jsondata = []

    # logic: getting the score_list for each in just one run
    color_score_list, idx_color_map, color_extra = get_result_test2(text_with_clean_catandbrand, idx_brand_map, idx_category_map, color_list, score_list)
    final_color = {}
    for d in color_score_list:
        if d in color_extra:
            if color_extra[d][2] > color_score_list[d][2] + 0.2:
                final_color[d] = color_extra[d]
            else:
                final_color[d] = color_score_list[d]
        else:
            final_color[d] = color_score_list[d]
    for d in color_extra:
        if d not in final_color:
            final_color[d] = color_extra[d]

    pattern_score_list, idx_pattern_map, pattern_extra = get_result_test2(text_with_clean_catandbrand, idx_brand_map, idx_category_map, pattern_list, score_list)
    final_pattern = {}
    for d in pattern_score_list:
        if d in pattern_extra:
            if pattern_extra[d][2] > pattern_score_list[d][2] + 0.2:
                final_pattern[d] = pattern_extra[d]
            else:
                final_pattern[d] = pattern_score_list[d]
        else:
            final_pattern[d] = pattern_score_list[d]
    for d in pattern_extra:
        if d not in final_pattern:
            final_pattern[d] = pattern_extra[d]

    material_score_list, idx_material_map, material_extra = get_result_test2(text_with_clean_catandbrand, idx_brand_map, idx_category_map, material_list, score_list)
    final_material = {}
    for d in material_score_list:
        if d in material_extra:
            if material_extra[d][2] > material_score_list[d][2] + 0.2:
                final_material[d] = material_extra[d]
            else:
                final_material[d] = material_score_list[d]
        else:
            final_material[d] = material_score_list[d]
    for d in material_extra:
        if d not in final_material:
            final_material[d] = material_extra[d]

    for s in score_list:
        brand_idx = s[0]
        brand = brand_bridge_map[idx_brand_map[s[0]]]

        cat_idx = s[1]
        cat_name = idx_category_map[s[1]]
        category = cat_bridge_map[cat_name]
        score = s[2]


        # print(brand_idx, brand, cat_idx,cat_name, category, score)
        c = None
        color_id = "no color"
        color_pair_score = 0

        for color_idx, record in final_color.items():
            if record[0] == brand_idx and idx_category_map[record[1]] == cat_name and record[2] > color_pair_score:
                c = idx_color_map[color_idx]
                color_id = get_detail_id(c)
                color_pair_score = record[2]

        p = None
        pattern_id = "no pattern"
        pattern_pair_score = 0

        for pattern_idx, record in final_pattern.items():
            if record[0] == brand_idx and record[1] == cat_idx and record[1] > pattern_pair_score:
                p = idx_pattern_map[pattern_idx]
                pattern_id = get_detail_id(p)
                pattern_pair_score = record[2]

        m = None
        material_id = "no material"
        material_pair_score = 0
        for material_idx, record in final_material.items():
            if record[0] == brand_idx and record[1] == cat_idx and record[2] > material_pair_score:
                m = idx_material_map[material_idx]
                material_id = get_detail_id(m)
                material_pair_score = record[2]

        data = {}
        data["Brand_Name"] = str(brand)
        data["CatName"] = str(cat_name)
        data["Category"] = str(category)
        data["brand_pair_score"] = float(score)

        details = []
        details.append({"color": c, "color_id": color_id,
                        "color_pair_score": color_pair_score,

                        "pattern": p, "pattern_id": pattern_id,
                        "patern_pair_score": pattern_pair_score,

                        "material": m, "material_id": material_id,
                        "material_pair_score": material_pair_score
                        })

        data["details"] = details
        jsondata.append(data)


    jsondata = sorted(jsondata, key=lambda i: i["brand_pair_score"], reverse=True)
    jsondata = sorted(jsondata, key= lambda i: i["Brand_Name"])

    return json.dumps(jsondata)

print('....          end          ....')

