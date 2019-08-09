#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 16:33:32 2019

@author: bingqingxie
"""

import csv

material_dict= {'canvas':'canvas', 'cashmere':'cashmere', 'chiffon':'chiffon', 'corduroy':'corduroy', 'jersey':'cotton',
                'supimacotton':'cotton', 'knit':'cotton', 'denim':'denim','jeans':'denim','jean':'denim', 'felted':'felt',
                'felt':'felt','plaid':'flannel','flannel':'flannel','fleece':'fleece','chambray':'chambray',
                'camel hair': 'fur', 'calfhair':'fur','camelhair':'fur','shearlig':'fur','cotton':'cotton',
                'goose':'goose', 'lacey':'lace','lace':'lace','calfskin':'leather','lambskin':'leather','goat':'leather',
                'cowhide':'leather','calf':'leather','lamb':'leather','goatskin':'leather','kangaroo':'leather','snakeskin':'leather',
                'python':'leather','snake':'leather','ostrich':'leather','alligator':'leather','gator':'leather','croc':'leather',
                'crocodile':'leather','linen':'linen','neoprene':'neoprene','rubber':'neoprene','satin':'satin','silk':'silk',
                'nubuck':'suede', 'suede':'suede','rayon':'synthetic', 'synthetic':'synthetic', 'spandex':'synthetic','viscose':'synthetic',
                'polyester':'synthetic','elastane':'synthetic','lycra':'synthetic','nylon':'synthetic', 'acrylic':'synthetic','acetate':'synthetic',
                'polyurethane':'synthetic','poly':'synthetic','manmade':'synthetic','man-made':'synthetic','plastic':'synthetic',
                'modal':'synthetic','eva':'synthetic','foam':'synthetic','velcro':'synthetic','lurex':'synthetic',
                'tulled': 'tulle', 'tulle':'tulle','tweed':'tweed', 'velvet':'velvet','wool':'wool','wooden':'wood'
                }

pattern_dict = {'print':'print', 'printed':'print', 'prints':'print', 'pattern':'print', 'patterned':'print', 'graphic':'print',\
'emboss':'emboss', 'embossed':'emboss', 'cloqué':'emboss','woven':'woven', 'weave':'woven', 'weaved':'woven', \
'wicker':'woven', 'wickered':'woven', 'embroidery':'woven', 'embroidered':'woven','ditsy':'ditsy','exotic':'exotic', \
'mix':'exotic', 'mixture':'exotic', 'floral':'floral','logo':'logo', 'brand':'logo', 'branded':'logo', 'signature':'logo', 
'paisley':'paisley','plaid':'plaid', 'checkered':'plaid', 'check':'plaid', 'flannel':'plaid',
'polka dot':'polka dot', 'polkadot':'polka dot', 'dots':'polka dot', 'spot':'polka dot', 'spotted':'polka dot',
'circle':'circle', 'circles':'circle', 'geometric':'circle','quilt':'quilt', 'quilted':'quilt', 'quilting':'quilt',\
'tie dye':'tie dye', 'tie dyed':'tie dye','tropical':'tropical', 'hawaiian':'tropical', 'hawaii':'tropical',\
'tiger':'leopard', 'lion':'leopard','panther':'leopard', 'leopard':'leopard', 'cheetah':'leopard','zebra':'zebra',\
'snake':'snake', 'snakeskin':'snake', 'python':'snake', 'croc':'snake', 'alligator':'snake','zig zag':'zigzag', \
'zig-zag':'zigzag', 'zigzag':'zigzag', 'chevron':'zigzag', 'feather':'feather', 'feathers':'feather','tribal':'tribal',\
'lace': 'lace', 'crochete': 'lace', 'crocheted': 'lace'}
'''
with open('material.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in material_dict.items():
       writer.writerow([key, value])
'''            
with open('pattern.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in pattern_dict.items():
       writer.writerow([key, value])          
            
            
            
            