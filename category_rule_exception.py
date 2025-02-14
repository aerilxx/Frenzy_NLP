#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 12:54:02 2019

@author: bingqingxie
"""

import csv
import re

# create map for pairing detailed key (ex long dress) to value (parent category) product
def create_category_pair():
    category_detail_dict = {}
    key = ''
    cat_list= []
    with open ('key_pair_category.csv','r') as infile:
        reader = csv.reader(infile)
     
        for row in reader:
            descriptive_category = row[0].split(',')
            main_category = row[1].split(',')
            value = row[2]
            
            for s in descriptive_category:
                ns = s.replace('-','').strip().lower()
                for j in main_category:
                    nj = j.replace('-','').strip().lower()
                    key = ns +' '+ nj 
                    category_detail_dict[key]=value
                    cat_list.append(key)
                    
    return category_detail_dict

# create rule exception dictionary
def rule_exception():
    rule_dict = {}
    rule = ''
    exception_list= []
    
    with open ('product_rule_exception.csv','r') as infile:
        reader = csv.reader(infile)
     
        for row in reader:
            keyword = row[1].split(',')
            products = row[2].split(',')
            parent_category = row[0]
            
            for s in keyword:
                ns = s.replace('-', '').strip().lower()
                for j in products:
                    nj = j.replace('-', '').strip().lower()
                    rule = ns+' '+nj
                    
                    if rule != ' ':
                        rule_dict[rule]=parent_category
                        exception_list.append(rule)
       
        
    return rule_dict, exception_list


rule_dict, rule_list = rule_exception()


def check_rule_exception(word, category_dict):
    category = ''
    # if product in exception list, it will be paring to the correct parent category
    
    exception_list = ['keyword product', 'short sleeve dress', 'short sleeve dresses', 'short sleeves dress', 'short sleeves dresses', 'pullover dress', 'pullover dresses', 'long sleeve dress', 'long sleeve dresses', 'long sleeves dress', 'long sleeves dresses', 'skirt dress', 'skirt dresses', 'skirts dress', 'skirts dresses', 'belt dress', 'belt dresses', 'belts dress', 'belts dresses', 'belt dress', 'belt dresses', 'belt dress', 'belt dresses', 'button-up dress', \
    'button-up dresses', 'button-down dress', 'button-down dresses', 'button up dress', 'button up dresses', 'button down dress', 'button down dresses', 'bra dress', 'bra dresses', 'bras dress', 'bras dresses', 'sweater dress', 'sweater dresses', 'coat dress', 'coat dresses', ' dress', ' dresses', 'shirt dress', 'shirt dresses', 'tank dress', 'tank dresses', 'short dress', 'short dresses', 'denim dress', 'denim dresses', 'jean dress', 'jean dresses', 'jeans dress', 'jeans dresses', 'short sleeve gown', 'short sleeve gowns', 'short sleeves gown', 'short sleeves gowns', 'pullover gown', 'pullover gowns', 'long sleeve gown', 'long sleeve gowns', 'long sleeves gown', 'long sleeves gowns', 'skirt gown', 'skirt gowns', 'skirts gown', 'skirts gowns', 'belt gown', 'belt gowns', 'belts gown', \
    'belts gowns', 'belt gown', 'belt gowns', 'belt gown', 'belt gowns', 'button-up gown', 'button-up gowns', 'button-down gown', 'button-down gowns', 'button up gown', 'button up gowns', 'button down gown', 'button down gowns', 'bra gown', 'bra gowns', 'bras gown', 'bras gowns', ' gown', ' gowns', 'denim top', 'denim tops', 'jean top', 'jean tops', 'jeans top', 'jeans tops', 'belt top', 'belt tops', 'belts top', 'belts tops', 'belt top', 'belt tops', 'belt top', 'belt tops', 'short top', 'short tops', 'short t-shirt', 'short tee', 'short t', 'slip on tank', 'slip on tanks', 'slip on top', 'slip on tops', 'slip ons tank', 'slip ons tanks', 'slip ons top', 'slip ons tops', 'slip tank', 'slip tanks', 'slip top', 'slip tops', 'tank tank', 'tank tanks', 'tank top', 'tank tops', ' tank', ' tanks', ' top', ' tops', 'dress shirt', 'dress shirts', 'dress- shirt', 'dress- shirts', 'denim shirt', 'denim shirts', 'jean shirt', 'jean shirts', 'short shirt', 'short shirts', 'o ford shirt', 'o ford shirts', 'sweat shirt', 'sweat shirts', 'button up coat', 'button up coats', 'button up parka', 
    'button up parkas', 'button up trench', 'button up trenches', 'button up trenchcoat', 'button up trenchcoats', 'button down coat', 'button down coats', 'button down parka', 'button down parkas', 'button down trench', 'button down trenches', 'button down trenchcoat', 'button down trenchcoats', 'button coat', 'button coats', 'button parka', 'button parkas', 'button trench', 'button trenches', 'button trenchcoat', \
    'button trenchcoats', 'belt coat', 'belt coats', 'belt parka', 'belt parkas', 'belt trench', 'belt trenches', 'belt trenchcoat', 'belt trenchcoats', 'belts coat', 'belts coats', 'belts parka', 'belts parkas', 'belts trench', 'belts trenches', 'belts trenchcoat', 'belts trenchcoats', 'belt coat', 'belt coats', 'belt parka', 'belt parkas', 'belt trench', 'belt trenches', 'belt trenchcoat', 'belt trenchcoats', 'belt coat', 'belt coats', 'belt parka', 'belt parkas', 'belt trench', 'belt trenches', 'belt trenchcoat', 'belt trenchcoats', 'short sleeve coat', 'short sleeve coats', 'short sleeve parka', 'short sleeve parkas', 'short sleeve trench', 'short sleeve trenches', 'short sleeve trenchcoat', 'short sleeve trenchcoats', 'short sleeves coat', 'short sleeves coats', 'short sleeves parka', 'short sleeves parkas', 'short sleeves trench', 'short sleeves trenches', 'short sleeves trenchcoat', 'short sleeves trenchcoats', 'long sleeve coat', 'long sleeve coats', 'long sleeve parka', 'long sleeve parkas', 'long sleeve trench', 'long sleeve trenches', 'long sleeve trenchcoat', \
    'long sleeve trenchcoats', 'long sleeves coat', 'long sleeves coats', 'long sleeves parka', 'long sleeves parkas', 'long sleeves trench', 'long sleeves trenches', 'long sleeves trenchcoat', 'long sleeves trenchcoats', 'denim coat', 'denim coats', 'denim parka', 'denim parkas', 'denim trench', 'denim trenches', 'denim trenchcoat', 'denim trenchcoats', 'jean coat', 'jean coats', 'jean parka', 'jean parkas', 'jean trench', 'jean trenches', 'jean trenchcoat', 'jean trenchcoats', 'jeans coat', 'jeans coats', 'jeans parka', 'jeans parkas', 'jeans trench', 'jeans trenches', 'jeans trenchcoat', 'jeans trenchcoats', 'short coat', 'short coats', 'short parka', 'short parkas', 'short trench', 'short trenches', 'short trenchcoat', 'short trenchcoats', 'duffle coat', 'duffle coats', 'duffle parka', \
    'duffle parkas', 'duffle trench', 'duffle trenches', 'duffle trenchcoat', 'duffle trenchcoats', 'button up jacket', 'button up jackets', 'button up kimono', 'button up kimonos', 'button up blazer', 'button up blazers', 'button down jacket', 'button down jackets', 'button down kimono', 'button down kimonos', 'button down blazer', 'button down blazers', 'button jacket', 'button jackets', 'button kimono', 'button kimonos', 'button blazer', 'button blazers', 'belt jacket', 'belt jackets', 'belt kimono', 'belt kimonos', 'belt blazer', 'belt blazers', 'belts jacket', 'belts jackets', 'belts kimono', 'belts kimonos', 'belts blazer', 'belts blazers', 'belt jacket', 'belt jackets', 'belt kimono', 'belt kimonos', 'belt blazer', 'belt blazers', 'belt jacket', 'belt jackets', 'belt kimono', 'belt kimonos', \
    'belt blazer', 'belt blazers', 'short sleeve jacket', 'short sleeve jackets', 'short sleeve kimono', 'short sleeve kimonos', 'short sleeve blazer', 'short sleeve blazers', 'short sleeves jacket', 'short sleeves jackets', 'short sleeves kimono', 'short sleeves kimonos', 'short sleeves blazer', 'short sleeves blazers', 'long sleeve jacket', 'long sleeve jackets', 'long sleeve kimono', 'long sleeve kimonos', 'long sleeve blazer', 'long sleeve blazers', 'long sleeves jacket', 'long sleeves jackets', 'long sleeves kimono', 'long sleeves kimonos', 'long sleeves blazer', 'long sleeves blazers', 'shawl jacket', 'shawl jackets', 'shawl kimono', 'shawl kimonos', 'shawl blazer', 'shawl blazers', 'shawls jacket', 'shawls jackets', 'shawls kimono', 'shawls kimonos', 'shawls blazer', 'shawls blazers', 'denim jacket', 'denim jackets', 'denim kimono', 'denim kimonos', 'denim blazer', 'denim blazers', 'jean jacket', 'jean jackets', 'jean kimono', 'jean kimonos', 'jean blazer', \
    'jean blazers', 'jeans jacket', 'jeans jackets', 'jeans kimono', 'jeans kimonos', 'jeans blazer', 'jeans blazers', 'short jacket', 'short jackets', 'short kimono', 'short kimonos', 'short blazer', 'short blazers', 'button up vest', 'button up vests', 'button up waistcoat', 'button up waistcoats', 'button up waist coat', 'button down vest', 'button down vests', 'button down waistcoat', 'button down waistcoats', 'button down waist coat', 'button vest', 'button vests', 'button waistcoat', 'button waistcoats', 'button waist coat', 'belt vest', 'belt vests', 'belt waistcoat', 'belt waistcoats', 'belt waist coat', 'belts vest', 'belts vests', 'belts waistcoat', 'belts waistcoats', 'belts waist coat', 'belt vest', 'belt vests', 'belt waistcoat', 'belt waistcoats', 'belt waist coat', 'belt vest', 'belt vests', 'belt waistcoat', 'belt waistcoats', 'belt waist coat', 'shawl vest', 'shawl vests', 'shawl waistcoat', 'shawl waistcoats', 'shawl waist coat', 'shawls vest', 'shawls vests', 'shawls waistcoat', 'shawls waistcoats', 'shawls waist coat', 'denim vest', 'denim vests', \
    'denim waistcoat', 'denim waistcoats', 'denim waist coat', 'jean vest', 'jean vests', 'jean waistcoat', 'jean waistcoats', 'jean waist coat', 'jeans vest', 'jeans vests', 'jeans waistcoat', 'jeans waistcoats', 'jeans waist coat', 'short vest', 'short vests', 'short waistcoat', 'short waistcoats', 'short waist coat', 'button up cape', 'button up capes', 'button up poncho', 'button up ponchos', 'button up cloak', 'button up cloaks', 'button down cape', 'button down capes', 'button down poncho', 'button down ponchos', 'button down cloak', 'button down cloaks', 'button cape', 'button capes', 'button poncho', 'button ponchos', 'button cloak', 'button cloaks', 'belt cape', 'belt capes', 'belt poncho', 'belt ponchos', 'belt cloak', 'belt cloaks', 'belts cape', 'belts capes', 'belts poncho', 'belts ponchos', 'belts cloak', 'belts cloaks', 'belt cape', 'belt capes', 'belt poncho', 'belt ponchos', 'belt cloak', 'belt cloaks', 'belt cape', 'belt capes', 'belt poncho', 'belt ponchos', 'belt cloak', 'belt cloaks', 'short sleeve cape', 'short sleeve capes', 'short sleeve poncho', \
    'short sleeve ponchos', 'short sleeve cloak', 'short sleeve cloaks', 'short sleeves cape', 'short sleeves capes', 'short sleeves poncho', 'short sleeves ponchos', 'short sleeves cloak', 'short sleeves cloaks', 'long sleeve cape', 'long sleeve capes', 'long sleeve poncho', 'long sleeve ponchos', 'long sleeve cloak', 'long sleeve cloaks', 'long sleeves cape', 'long sleeves capes', 'long sleeves poncho', 'long sleeves ponchos', 'long sleeves cloak', 'long sleeves cloaks', 'denim cape', 'denim capes', 'denim poncho', 'denim ponchos', 'denim cloak', 'denim cloaks', 'jean cape', 'jean capes', 'jean poncho', 'jean ponchos', 'jean cloak', 'jean cloaks', 'jeans cape', 'jeans capes', 'jeans poncho', 'jeans ponchos', 'jeans cloak', 'jeans cloaks', 'short cape', 'short capes', 'short poncho', 'short ponchos', 'short cloak', 'short cloaks', ' cape', ' capes', ' poncho', ' ponchos', ' cloak', ' cloaks', 'denim skirt', 'denim skirts', 'jean skirt', 'jean skirts', 'jeans skirt', 'jeans skirts', 'belt skirt', 'belt skirts', 'belts skirt', 'belts skirts', 'belt skirt', 'belt skirts', 'belt skirt', 'belt skirts', 'button-up skirt', 'button-up skirts', 'button-down skirt', 'button-down skirts', 'button up skirt', 'button up skirts', 'button down skirt', 'button down skirts', ' skirt', ' skirts', 'denim miniskirt', 'denim miniskirts', 'jean miniskirt', 'jean miniskirts', 'jeans miniskirt', 'jeans miniskirts', 'belt miniskirt', 'belt miniskirts', 'belts miniskirt', 'belts miniskirts', 'belt miniskirt', 'belt miniskirts', 'belt miniskirt', 'belt miniskirts', 'button-up miniskirt', 'button-up miniskirts', 'button-down miniskirt', 'button-down miniskirts', 'button up miniskirt', 'button up miniskirts', 'button down miniskirt', 'button down miniskirts', 'denim miniskirt', 'denim miniskirts', 'jean miniskirt', 'jean miniskirts', 'jeans miniskirt', 'jeans miniskirts', 'short miniskirt', 'short miniskirts', 'denim midiskirt', 'denim midiskirts', 'denim midi-skirt', 'denim midi-skirts', 'jean midiskirt', 'jean midiskirts', 'jean midi-skirt', 'jean midi-skirts', 'jeans midiskirt', 'jeans midiskirts', 'jeans midi-skirt', 'jeans midi-skirts', 'belt midiskirt', 'belt midiskirts', 'belt midi-skirt', 'belt midi-skirts', 'belts midiskirt', 'belts midiskirts', 'belts midi-skirt', 'belts midi-skirts', 'belt midiskirt', 'belt midiskirts', 'belt midi-skirt', 'belt midi-skirts', 'belt midiskirt', 'belt midiskirts', 'belt midi-skirt', 'belt midi-skirts', 'button-up midiskirt', 'button-up midiskirts', 'button-up midi-skirt', 'button-up midi-skirts', 'button-down midiskirt', 'button-down midiskirts', 'button-down midi-skirt', 'button-down midi-skirts', 'button up midiskirt', 'button up midiskirts', 'button up midi-skirt', 'button up midi-skirts', 'button down midiskirt', 'button down midiskirts', 'button down midi-skirt', 'button down midi-skirts', ' midiskirt', ' midiskirts', ' midi-skirt', ' midi-skirts', 'denim ma iskirt', 'denim ma i-skirt', 'denim ma i-skirts', 'jean ma iskirt', 'jean ma i-skirt', 'jean ma i-skirts', 'jeans ma iskirt', 'jeans ma i-skirt', 'jeans ma i-skirts', 'belt ma iskirt', 'belt ma i-skirt', 'belt ma i-skirts', 'belts ma iskirt', 'belts ma i-skirt', 'belts ma i-skirts', 'belt ma iskirt', 'belt ma i-skirt', 'belt ma i-skirts', 'belt ma iskirt', 'belt ma i-skirt', 'belt ma i-skirts', 'button-up ma iskirt', 'button-up ma i-skirt', 'button-up ma i-skirts', 'button-down ma iskirt', 'button-down ma i-skirt', 'button-down ma i-skirts', 'button up ma iskirt', 'button up ma i-skirt', 'button up ma i-skirts', 'button down ma iskirt', 'button down ma i-skirt', 'button down ma i-skirts', 'belt short', 'belt shorts', 'belts short', 'belts shorts', 'belt short', 'belt shorts', 'denim short', 'denim shorts', 'jean short', 'jean shorts', 'jeans short', 'jeans shorts', 'button-up short', 'button-up shorts', 'button-down short', 'button-down shorts', 'button up short', 'button up shorts', 'button down short', 'button down shorts', 'chino short', 'chino shorts', 'chinos short', 'chinos shorts', 'denim skort', 'denim skorts', 'jean skort', 'jean skorts', 'jeans skort', 'jeans skorts', 'belt skort', 'belt skorts', 'belts skort', 'belts skorts', 'belt skort', 'belt skorts', 'belt skort', 'belt skorts', 'button-up skort', 'button-up skorts', 'button-down skort', 'button-down skorts', 'button up skort', 'button up skorts', 'button down skort', 'button down skorts', 'belt jean', 'belt jeans', 'belt denim', 'belts jean', 'belts jeans', 'belts denim', 'belt jean', 'belt jeans', 'belt denim', 'belt jean', 'belt jeans', 'belt denim', 'button-up jean', 'button-up jeans', 'button-up denim', 'button-down jean', 'button-down jeans', 'button-down denim', 'button up jean', 'button up jeans', 'button up denim', 'button down jean', 'button down jeans', 'button down denim', 'boot jean', 'boot jeans', 'boot denim', 'belt pant', 'belt pants', 'belt trousers', 'belt trouser', 'belt slack', 'belt slacks', 'belt chino', 'belt chinos', 'belts pant', 'belts pants', 'belts trousers', 'belts trouser', 'belts slack', 'belts slacks', 'belts chino', 'belts chinos', 'belt pant', 'belt pants', 'belt trousers', 'belt trouser', 'belt slack', 'belt slacks', 'belt chino', 'belt chinos', 'flat pant', 'flat pants', 'flat trousers', 'flat trouser', 'flat slack', 'flat slacks', 'flat chino', 'flat chinos', 'flat pant', 'flat pants', 'flat trousers', 'flat trouser', 'flat slack', 'flat slacks', 'flat chino', 'flat chinos', 'o ford pant', 'o ford pants', 'o ford trousers', 'o ford trouser', 'o ford slack', 'o ford slacks', 'o ford chino', 'o ford chinos', 'dress pant', 'dress pants', 'dress trousers', 'dress trouser', 'dress slack', 'dress slacks', 'dress chino', 'dress chinos', 'boot pant', 'boot pants', 'boot trouser', 'boot trousers', 'boot slack', 'boot slacks', 'boot chino', 'boot chinos', 'jump suits', 'jump suit', 'play suits', 'play suit', 'body suits', 'body suit', 'denim jumper', 'denim jumpers', 'denim jumpsuit', 'denim jumpsuits', 'denim romper', 'denim rompers', 'denim jumpsuit', 'denim jumpsuits', 'denim jump-suit', 'denim jump-suits', 'denim playsuit', 'denim playsuits', 'denim play-suit', 'denim play-suits', 'denim bodysuits', 'denim bodysuit', 'denim body-suit', 'denim body-suits', 'denim jump suit', 'denim jump suits', 'denim play suit', 'denim play suits', 'denim body suit', 'denim body suits', 'denim overall', 'denim overalls', 'denim over-all', 'denim over-alls', 'denim dungarees', 'denim dungaree', 'denim shortall', 'denim shortalls', 'denim short-all', 'denim short-alls', 'jeans jumper', 'jeans jumpers', 'jeans jumpsuit', 'jeans jumpsuits', 'jeans romper', 'jeans rompers', 'jeans jumpsuit', 'jeans jumpsuits', 'jeans jump-suit', 'jeans jump-suits', 'jeans playsuit', 'jeans playsuits', 'jeans play-suit', 'jeans play-suits', 'jeans bodysuits', 'jeans bodysuit', 'jeans body-suit', 'jeans body-suits', 'jeans jump suit', 'jeans jump suits', 'jeans play suit', 'jeans play suits', 'jeans body suit', 'jeans body suits', 'jeans overall', 'jeans overalls', 'jeans over-all', 'jeans over-alls', 'jeans dungarees', 'jeans dungaree', 'jeans shortall', 'jeans shortalls', 'jeans short-all', 'jeans short-alls', 'jean jumper', 'jean jumpers', 'jean jumpsuit', 'jean jumpsuits', 'jean romper', 'jean rompers', 'jean jumpsuit', 'jean jumpsuits', 'jean jump-suit', 'jean jump-suits', 'jean playsuit', 'jean playsuits', 'jean play-suit', 'jean play-suits', 'jean bodysuits', 'jean bodysuit', 'jean body-suit', 'jean body-suits', 'jean jump suit', 'jean jump suits', 'jean play suit', 'jean play suits', 'jean body suit', 'jean body suits', 'jean overall', 'jean overalls', 'jean over-all', 'jean over-alls', 'jean dungarees', 'jean dungaree', 'jean shortall', 'jean shortalls', 'jean short-all', 'jean short-alls', 'bra top', 'bra tops', 'short sleeve robe', 'short sleeve robes', 'short sleeve kimono', 'short sleeve kimonos', 'short sleeves robe', 'short sleeves robes', 'short sleeves kimono', 'short sleeves kimonos', 'long sleeve robe', 'long sleeve robes', 'long sleeve kimono', 'long sleeve kimonos', 'long sleeves robe', 'long sleeves robes', 'long sleeves kimono', 'long sleeves kimonos', 'denim bikini', 'denim bikinis', 'denim tankini', 'jean bikini', 'jean bikinis', 'jean tankini', 'jeans bikini', 'jeans bikinis', 'jeans tankini', 'bikini top', 'bikini tops', 'bikini bra', 'bikini bralette', 'bikinis top', 'bikinis tops', 'bikinis bra', 'bikinis bralette', 'tankini top', 'tankini tops', 'tankini bra', 'tankini bralette', 'swim top', 'swim tops', 'swim bra', 'swim bralette', 'swimwear top', 'swimwear tops', 'swimwear bra', 'swimwear bralette', 'bathing suit top', 'bathing suit tops', 'bathing suit bra', 'bathing suit bralette', 'bathingsuit top', 'bathingsuit tops', 'bathingsuit bra', 'bathingsuit bralette', 'bathing top', 'bathing tops', 'bathing bra', 'bathing bralette', 'swimsuit top', 'swimsuit tops', 'swimsuit bra', 'swimsuit bralette', 'swim top', 'swim tops', 'swim bra', 'swim bralette', 'wet dress', 'wet dresses', 'wet suit', 'wet suits', 'swim dress', 'swim dresses', 'swim suit', 'swim suits', 'wet suit', 'wet suits', 'denim shoe', 'denim shoes', 'jean shoe', 'jean shoes', 'jeans shoe', 'jeans shoes', 'top shoe', 'top shoes', 'tops shoe', 'tops shoes', 'top shoe', 'top shoes', 'tops shoe', 'tops shoes', 'top shoe', 'top shoes', 'dress boot', 'dress boots', 'dress bootie', 'dress booties', 'denim boot', 'denim boots', 'denim bootie', 'denim booties', 'jeans boot', 'jeans boots', 'jeans bootie', 'jeans booties', 'jean boot', 'jean boots', 'jean bootie', 'jean booties', 'denim mules', 'denim mule', 'denim clog', 'denim clogs', 'jeans mules', 'jeans mule', 'jeans clog', 'jeans clogs', 'jean mules', 'jean mule', 'jean clog', 'jean clogs', 'denim loafers', 'denim loafer', 'denim mocassins', 'denim mocassin', 'jean loafers', 'jean loafer', 'jean mocassins', 'jean mocassin', 'jeans loafers', 'jeans loafer', 'jeans mocassins', 'jeans mocassin', 'dress shoes', 'dress shoe', 'dress- shoes', 'dress- shoe', 'denim pump', 'denim pumps', 'denim heel', 'denim heels', 'denim high-heel', 'denim high-heels', 'denim courts', 'jeans pump', 'jeans pumps', 'jeans heel', 'jeans heels', 'jeans high-heel', 'jeans high-heels', 'jeans courts', 'jean pump', 'jean pumps', 'jean heel', 'jean heels', 'jean high-heel', 'jean high-heels', 'jean courts', 'hair pump', 'hair pumps', 'hair heel', 'hair heels', 'hair high-heel', 'hair high-heels', 'hair courts', 'denim sandal', 'denim sandals', 'denim gladiator', 'denim gladiators', 'denim flip flop', 'denim flip flops', 'denim flip-flop', 'denim flip-flops', 'denim slide', 'denim slides', 'denim slider', 'jean sandal', 'jean sandals', 'jean gladiator', 'jean gladiators', 'jean flip flop', 'jean flip flops', 'jean flip-flop', 'jean flip-flops', 'jean slide', 'jean slides', 'jean slider', 'jeans sandal', 'jeans sandals', 'jeans gladiator', 'jeans gladiators', 'jeans flip flop', 'jeans flip flops', 'jeans flip-flop', 'jeans flip-flops', 'jeans slide', 'jeans slides', 'jeans slider', 'thong sandal', 'thong sandals', 'thong gladiator', 'thong gladiators', 'thong flip flop', 'thong flip flops', 'thong flip-flop', 'thong flip-flops', 'thong slide', 'thong slides', 'thong slider', 'denim wedges', 'denim wedge', 'jean wedges', 'jean wedge', 'jeans wedges', 'jeans wedge', 'denim platforms', 'denim platform', 'jean platforms', 'jean platform', 'jeans platforms', 'jeans platform', 'denim sneaker', 'denim sneakers', 'denim trainers', 'denim trainer', 'jean sneaker', 'jean sneakers', 'jean trainers', 'jean trainer', 'jeans sneaker', 'jeans sneakers', 'jeans trainers', 'jeans trainer', 'top sneaker', 'top sneakers', 'top trainers', 'top trainer', 'tops sneaker', 'tops sneakers', 'tops trainers', 'tops trainer', 'top sneaker', 'top sneakers', 'top trainers', 'top trainer', 'hair head wrap', 'iphone ', 'iphone6 plus ', 'rolling brief', 'top bag', 'top bags', 'top handbag', 'top handbags', 'top hand-bag', 'top hand bag', 'top hand bags', 'top purse', 'top purses', 'top pouch', 'tops bag', 'tops bags', 'tops handbag', 'tops handbags', 'tops hand-bag', 'tops hand bag', 'tops hand bags', 'tops purse', 'tops purses', 'tops pouch', 'handle bag', 'handle bags', 'handle handbag', 'handle handbags', 'handle hand-bag', 'handle hand bag', 'handle hand bags', 'handle purse', 'handle purses', 'handle pouch', 'top handles bag', 'top handles bags', 'top handles handbag', 'top handles handbags', 'top handles hand-bag', 'top handles hand bag', 'top handles hand bags', 'top handles purse', 'top handles purses', 'top handles pouch', 'flat bag', 'flat bags', 'flat handbag', 'flat handbags', 'flat hand-bag', 'flat hand bag', 'flat hand bags', 'flat purse', 'flat purses', 'flat pouch', 'belt bag', 'belt bags', 'belt handbag', 'belt handbags', 'belt hand-bag', 'belt hand bag', 'belt hand bags', 'belt purse', 'belt purses', 'belt pouch', 'denim bag', 'denim bags', 'denim handbag', 'denim handbags', 'denim hand-bag', 'denim hand bag', 'denim hand bags', 'denim purse', 'denim purses', 'denim pouch', 'petite bag', 'petite bags', 'petite handbag', 'petite handbags', 'petite hand-bag', 'petite hand bag', 'petite hand bags', 'petite purse', 'petite purses', 'petite pouch', 'top clutch', 'top clutches', 'tops clutch', 'tops clutches', 'top- clutch', 'top- clutches', 'top handle clutch', 'top handle clutches', 'top handles clutch', 'top handles clutches', 'flat clutch', 'flat clutches', 'denim clutch', 'denim clutches', 'petite clutch', 'petite clutches', 'top tote', 'top totes', 'top duffle', 'top duffles', 'top duffels', 'top duffel', 'top carryall', 'top holdall', 'top shopper', 'top shoppers', 'tops tote', 'tops totes', 'tops duffle', 'tops duffles', 'tops duffels', 'tops duffel', 'tops carryall', 'tops holdall', 'tops shopper', 'tops shoppers', 'top- tote', 'top- totes', 'top- duffle', 'top- duffles', 'top- duffels', 'top- duffel', 'top- carryall', 'top- holdall', 'top- shopper', 'top- shoppers', 'top handle tote', 'top handle totes', 'top handle duffle', 'top handle duffles', 'top handle duffels', 'top handle duffel', 'top handle carryall', 'top handle holdall', 'top handle shopper', 'top handle shoppers', 'top handles tote', 'top handles totes', 'top handles duffle', 'top handles duffles', 'top handles duffels', 'top handles duffel', 'top handles carryall', 'top handles holdall', 'top handles shopper', 'top handles shoppers', 'denim tote', 'denim totes', 'denim duffle', 'denim duffles', 'denim duffels', 'denim duffel', 'denim carryall', 'denim holdall', 'denim shopper', 'denim shoppers', 'petite tote', 'petite totes', 'petite duffle', 'petite duffles', 'petite duffels', 'petite duffel', 'petite carryall', 'petite holdall', 'petite shopper', 'petite shoppers', 'top satchel', 'top satchels', 'tops satchel', 'tops satchels', 'top- satchel', 'top- satchels', 'top handle satchel', 'top handle satchels', 'top handles satchel', 'top handles satchels', 'denim satchel', 'denim satchels', 'petite satchel', 'petite satchels', 'top crossbody', 'top crossbodies', 'top cross-body', 'top cross body', 'top across body', 'top crossbag', 'top across-body', 'top ', 'tops crossbody', 'tops crossbodies', 'tops cross-body', 'tops cross body', 'tops across body', 'tops crossbag', 'tops across-body', 'tops ', 'top- crossbody', 'top- crossbodies', 'top- cross-body', 'top- cross body', 'top- across body', 'top- crossbag', 'top- across-body', 'top- ', 'top handle crossbody', 'top handle crossbodies', 'top handle cross-body', 'top handle cross body', 'top handle across body', 'top handle crossbag', 'top handle across-body', 'top handle ', 'top handles crossbody', 'top handles crossbodies', 'top handles cross-body', 'top handles cross body', 'top handles across body', 'top handles crossbag', 'top handles across-body', 'top handles ', 'denim crossbody', 'denim crossbodies', 'denim cross-body', 'denim cross body', 'denim across body', 'denim crossbag', 'denim across-body', 'denim ', 'petite crossbody', 'petite crossbodies', 'petite cross-body', 'petite cross body', 'petite across body', 'petite crossbag', 'petite across-body', 'petite ', 'top hobo', 'top hobos', 'tops hobo', 'tops hobos', 'top- hobo', 'top- hobos', \
    'top handle hobo', 'top handle hobos', 'top handles hobo', 'top handles hobos', 'denim hobo', 'denim hobos', 'petite hobo', 'petite hobos', 'stud ', 'studs ', 'baguette ring', 'baguette rings', 'bracelet watch', 'bracelet watches', 'bracelet timepiece', 'bracelet wristwatch', 'bracelet time teller', 'bracelet ', 'bracelets watch', 'bracelets watches', 'bracelets timepiece', 'bracelets wristwatch', 'bracelets time teller', 'bracelets ', 'wrist strap watch', 'wrist strap watches', 'wrist strap timepiece', 'wrist strap wristwatch', 'wrist strap time teller', 'wrist strap ', 'wristtrap watch', 'wristtrap watches', 'wristtrap timepiece', 'wristtrap wristwatch', 'wristtrap time teller', 'wristtrap ', 'wrist-strap watch', 'wrist-strap watches', 'wrist-strap timepiece', 'wrist-strap wristwatch', 'wrist-strap time teller', 'wrist-strap ', 'mud mask', 'face mask', 'body wash', 'foot wash', 'top gloss', 'top coat']

    
    if word in exception_list:
        category = rule_dict[word]
    else:
        category = category_dict[word]

    return category


# construct one to one dictionay
def create_category_dictionary():
    category_dict={}  
    
    with open ('category_pair.csv','r') as infile:
        reader = csv.reader(infile)
     
        for row in reader:
            sub_category = row[1].split(',')
            main_category = row[0]
          
            for s in sub_category:
                ns = s.replace('-', '').strip().lower()
                if s is None:
                    category_dict[main_category.lower().strip()] = main_category.lower().strip()
                else: 
                    category_dict[ns]=main_category.lower().strip()
        
    return category_dict


def multi_word_category_dictionary(): 
    category_dict = create_category_dictionary()
    detailed_dict = create_category_pair()
    category_dict.update(detailed_dict)
    category_dict.update(rule_dict)
    
    one_word_dict = {}
    two_word_dict = {}
    three_word_dict = {}
    four_word_dict = {}
    
    for key, value in category_dict.items():
        count = len(re.findall(r'\w+', key))
        if count ==2:
            two_word_dict[key] = value
        elif count == 3:
            three_word_dict[key] = value
        elif count == 4:
            four_word_dict[key] = value
        else:
            one_word_dict[key] = value
    
    return one_word_dict, two_word_dict, three_word_dict, four_word_dict
    
    

one_word_dict, two_word_dict, three_word_dict, four_word_dict= multi_word_category_dictionary()

with open('1_word_category.txt', 'w') as file:
    file.write(str(one_word_dict))

with open('2_word_category.txt', 'w') as file:
    file.write(str(two_word_dict))

with open('3_word_category.txt', 'w') as file:
    file.write(str(three_word_dict))    

with open('4_word_category.txt', 'w') as file:
    file.write(str(four_word_dict))