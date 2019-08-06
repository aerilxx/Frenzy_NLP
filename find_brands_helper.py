#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:51:49 2019

@author: bingqingxie
"""

import nltk
from nltk.tokenize import sent_tokenize
from nltk.util import ngrams
import ast

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

def pre_clean_text(text):
    # logic: just finding all ascii possible values and ignoring the rest like '…'
    text = ''.join([i if ord(i) < 256 else ' ' for i in text])
    # text = text.encode('ascii', 'ignore').decode('ascii')
    text = ' '.join(text.split())
    # replace special puncutation with. in original text 
    t = text.replace('-', ' ').replace('–',' ').replace(':', ' ').replace('(', ' ').replace(')', ' '). \
        replace('~', ' ').replace(';', '.').replace('&', ' ').replace('+', ' '). \
        replace('/', ' ').replace('|', '.').replace('!', '.').replace('?', '.').replace('’',"'").replace(',', ' , ')

    '''
change brands name have french word
    replace("Á","a").replace("á","a").replace("Ä","a").replace("ä","a").replace("É","e").\
    replace("é","e").replace("Ë","e").replace("ë","e").replace("Í","i").replace("ï","i").\
    replace("í","i").replace("Ï","i").replace("Ó","o").replace("ó","o").replace("Ö","o").\
    replace("ö","o").replace("Ú","u").replace("ú","u").replace("Ü","u").replace("ü","u").replace("’", "'")
    '''

    for key, value in material_dict.items():
        t = t.replace(key, value)
    '''
    for key,value in pattern_dict.items():
        t = t.replace(key,value)
    '''
    return t


def pre_clean_text_brands(text):
    # delete extra white space
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = ' '.join(text.split())
    # replace special puncutation with. in brands with special cases 
    t = text.replace('-', '').replace('–','').replace(':', '').replace('(', '').replace(')', ''). \
        replace('~', '').replace(';', '').replace('&', '').replace('+', ''). \
        replace('/', '').replace('|', '').replace('!', '').replace('?', '').replace('.','').replace('%','')

    '''
change brands name have french word
    replace("Á","a").replace("á","a").replace("Ä","a").replace("ä","a").replace("É","e").\
    replace("é","e").replace("Ë","e").replace("ë","e").replace("Í","i").replace("ï","i").\
    replace("í","i").replace("Ï","i").replace("Ó","o").replace("ó","o").replace("Ö","o").\
    replace("ö","o").replace("Ú","u").replace("ú","u").replace("Ü","u").replace("ü","u").replace("’", "'")
    '''
    return t

#read txt dictioanry files
brand_dict={}
with open ('brands.txt','r',encoding="utf-8") as infile:
    brand_dict = ast.literal_eval(infile.readline())

def upper_dict(d):
   new_dict = dict((k.capitalize(), v.capitalize()) for k, v in d.items())
   return new_dict 

def after_clean_text(text):
    text2 = ""
        
    for s in sent_tokenize(text):
        # use abc as the substitute of . in order to corresponds to sentence map
        ns = s.replace('.',' abc ')
        text2+=(''+ns)
        
    return text2

#find all brands (limit set in brand dictionary) in the text
    # Brands must be capitalized
def find_brands_without_punc(text):
    # words = word_tokenize(text)
    text = text.replace('.',' . ')
    words = list(text.split(' '))
    res = []
    for word in words:
        if len(word) > 0:
            res.append(word)
    words = res

    brands=[]
    upper_d = upper_dict(brand_dict)
    
    for w in words:
        if w[0].isupper() and w.capitalize() in upper_d:
            # special cases with all uppercase brand individually check
            excludes = ['Suit', 'It', 'Best', 'True', 'Contact', 'Boots', 'Ball', 'Block', 'IT', 'Trend', 'Love', 'Blend', 'NOW','Line','Wardrobe','Eye','Pieces','Details',\
                        'Think','Me','Day','Flowers','Fresh','Match','Simple','Toss','Classic','Gorgeous','Office','Only','Combo','Head Over Heels','Punch','Head','Together',\
                        'Trend','Black','Keep','Fallen','Accessories','Move','Town','Plus','List','IN BED', 'VS', 'Aspects', 'Springs', 'Made', 'Eight', 'Kind', 'Fortune', 'Block',\
                        'Seek', 'Staple', 'SET', 'Reason', 'Privilege', 'Living', 'Discovery', 'Space', 'SuperStar', 'Marvel', 'Debut', 'NOW', 'Day', 'Globe', 'Hope', 'ADD', 'POP',\
                        'Fab', 'Nordstrom', 'Canvas', 'O', 'Unique', 'Sicily', 'Boutique', 'Sequin', 'Sparkle', 'Next', 'Holiday', 'Wrapper', 'Sky', 'DC', 'Menu', 'Element', 'Elements',\
                        'Mini', 'All Black', 'TP', 'Christina', 'So Easy', 'Mine', 'Hue', 'Bell', 'Darling', 'Name', 'Super', 'Fits', 'Perfection', 'Blazer', 'Jump', 'MET', 'IDEA', 'totes',\
                        'Chi', 'Rose', 'Wonders', 'Degree', 'Barbie', 'Charisma', 'Stellar', 'CAT', 'Republic', 'Ring', 'Rio', 'BOB', 'Gosh', 'Singer', 'Just For You', 'Character',\
                        'Only One', 'Native', 'Justice', 'Diana', 'One Piece', 'Young', 'Image', 'Your Own', 'Wanted', 'Solid', 'Olympia', 'JET', 'Casting', 'Lauren', 'Holmes', \
                        'Kate', 'Laura', 'Oliver', 'Nina', 'Ricci', 'Thomas', 'Wish', 'Closet', 'Helena', 'Living', 'FLY', 'OAK', 'Little Big', 'Frank', 'Laundry', 'Earth', 'Spring Air',\
                        'Kiss', 'Phenomenon', 'Limited Edition', 'Jordan', 'Town', 'Become', 'Sugar', 'Bloom', 'Area', 'Storm', 'Adore', 'Co']
            if w in excludes:
                pass
            else:
                brands.append(w.capitalize())
            # print("1 word brand is : " + w)
       
    for w in list(nltk.bigrams(words)):
        pair = list(w)
        str1 = ' '.join(pair)
        s = str1.capitalize()

    # added this line to avoid string starting with smaller case getting identified as brand in n-grams
        if str1[0].isupper() and s in upper_d:
            brands.append(s)

    for w in list(nltk.trigrams(words)):
        pair = list(w)
        str1 = ' '.join(pair)
        s = str1.capitalize()
        if str1[0].isupper() and s in upper_d:
            brands.append(s)

    fourgrams = ngrams(words,4)
    for w in list(fourgrams):
        pair = list(w)
        str1 = ' '.join(pair)
        s = str1.capitalize()

        if str1[0].isupper() and s in upper_d:
            brands.append(s)

    fivegrams = ngrams(words,5)
    for w in list(fivegrams):
        pair = list(w)
        str1 = ' '.join(pair)
        s = str1.capitalize()

        if str1[0].isupper() and s in upper_d:
            brands.append(s)

    sixgrams = ngrams(words,6)
    for w in list(sixgrams):
        pair = list(w)
        str1 = ' '.join(pair)
        s = str1.capitalize()

        if str1[0].isupper() and s in upper_d:
            brands.append(s)
    print("without punc brands")
    print(brands)
    return brands

# inpt text must be raw text
def find_brands_with_specialcase(text):
    brands_arr = brand_dict.keys()
    brands = []
    
    #brands ending with . will be treat without last . in tokenize
    for b in brands_arr:
        if b.endswith('.'):
            brands.append(b)
            
    #brands with %  & etc speical cases
    for b in brands_arr:
        if '%' in b \
        or '&' in b \
        or '.' in b \
        or '+' in b \
        or '@' in b \
        or '/' in b \
        or " ' " in b \
        or '-' in b:
            brands.append(b)

    # brands with !
    special_brands = ['Ic! Berlin', 'bravado! designs', 'joop! time', 'joop! jeans', \
                      'stop staring!', 'h! by henry holland', 'Think!', 'Lights Up!' ,\
                      'JOOP!', 'D-S!de', 'Baby!', 'Me! Bath', 'Supergoop!']

    #brands with ', need to be different from ordinay '
    special_brands2 = ["converse women's", "dockers men's", "joe's jeans kids", "the pant by joe's jeans", "the tee by joe's jeans", "the shirt by joe's jeans", "joe's", "levi's vintage clothing", "levi's red tab", "lady levi's", "levi's engineered jeans", "levi's® red tab", "levi's kidswear", "levi's®", "levi's® juniors", "levi's® mens", "levi's blue", "levi's handbags", "junya watanabe comme des garçons man x levi's", "levi's eco", "levi's made & crafted", "levi's® guys", "nordstrom men's shop", "ralph lauren women's polo", "steve madden's fix*", "fleur't lingerie", "jean's paul gaultier", "dr.scholl's", "gf ferre'", "ferre'", "ferre' jeans", "l' occitane", "paul smith women's accessories", "paul smith men's accessories", "saks fifth avenue men's collection", "tod's for ferrari", "tod's junior", "t project by tod's", "dream angels by victoria's secret", "glamour by victoria's secret", "angels by victoria's secret", "o'neill wetsuits", "bric's u.s.a.", "designer's touch kids", "l'artisan", "l' autre chose", "palomitas by paloma barcelo'", "smith's rosebud salve", "bath & body works® men's", "kiehl's since 1851", "kiehl's since", "l'oreal elvive", "serie expert by l'oreal", "techni.art by l'oreal", "l'oreal paris", "tecni.art by l'oreal", "l'oréal professionnel", "palmer's", "penhaligon's", "christy's", "c'n'c' costume national", "chef'schoice", "chef'n", "emma hope's shoes", "l'aromarine fragrances", "marc o'polo junior", "nicolo' ceschi berrini", "meltin'pot", "pantofola d'oro - instant collection", "stussy men's", "gold 'n hot", "jen's pirate booty", "arm's reach concepts", "gerber children's wear", "oshkosh b'gosh", "oshkosh b'gosh boys", "grazia'lliani lingeria", "b.tempt'd by wacoal", "shelly's shoes", "tomorrowland (women's)", "aldo brue'", "o'gio", "sara's prints kids", "l'agent", "'47 brand", "maison margiela - collection printemps ete'", "hero's", "paul's boutique", "fish 'n' chips", "marithe' f. girbaud", "ljd marithe' francois girbaud", "Tod's", "Victoria's Secret", "Quark's", "O'Neill", "Chico's", "Bric's", "Designer's Touch", "L'Artisan Parfumeur", "L'Autre Chose", "Pepper's", "It's Our Time", "Carol's Daughter", "Joe's Jeans", "L'Wren Scott", "Ben's Garden", "Burt's Bees", "Dickinson's", "Kiehl's", "L'Oreal", "Lands' End", "Mrs. Meyer's", "Nature's Gate", "Levi's", "De'Longhi", "Hershey's", "P'kolino", "Chef's Choice", "Johnson's Baby", "O'Keeffe's", "Chef'N", "L'Abitare", "Robin's Jeans", "Africa's Best", "Alessandro Dell'Acqua", "Dr. Bronner's", "Dr. Miracle's", "Dr. Singha's", "Dr. Tung's", "Earth's Best", "Hyland's", "L'Aromarine", "L'Aromatheque", "Luster's", "Mane 'N Tail", "Mitchell's", "Mommy's Bliss", "Murray's", "Nature's Answer", "Nature's Way", "One 'N Only", "Papo d'Anjo", "Smith's", "Sof' Feet", "Tom's of Maine", "Marc O'Polo", "Sofie D'hoore", "Marina D'Este", "Etat Libre d'Orange", "Gentlemen's Tonic", "John Allan's", "A Priorite'", "CAFe'NOIR", "Fauzian Jeunesse'", "Gaudi'", "Gio' Moretti", "Henry Cotton's", "J's Exte'", "Warner's", "Joy's", "Pantofola D'oro", "Poisson D'amour", "Rose' A Pois", "Vigano'", "Gold'n Hot", "L'anza", "Woody's", "Pom D'Api", "Chef's Planet", "Richard's Homewares", "Baby K'tan", "Children's Apparel Network", "Nature's Baby", "Eau d'Italie", "Manufacture D'essai", "Y's", "Caran d'Ache", "black'Up", "I'coo", "Raison D'etre", "Andrea D'Amico", "Grazia'Lliani", "I'M Isola Marras", "Lorna Bose'", "Pierre Darre'", "Tricker's", "B.Tempt'd", "Doucal's", "Innue'", "Rada'", "L'amour", "Church's", "Arc'teryx", "D+art's", "Dr. Scholl's", "L'ge", "L'Agence", "Es'givien", "It's Met", "Jeordie's", "Carter's", "Pool'", "Theyskens' Theory", "Sara's Prints", "Bless'ed Are The Meek", "Cathy's Concepts", "Harry's of London", "Pez D'or", "Rubie's Costume Co", "Traveler's Choice", "Heal's", "O'Neill Swimwear", "Ach'e", "L'Agent by Agent Provocateur", "Frankie's Bikinis", "Issa de' mar", "'47", "L'OBJET", "L'Occitane", "Gilligan & O'Malley", "Hero's Heroine", "Dek'her", "Ekle'", "Jei O'", "O'2nd", "Paula's Choice", "Scotch R'Belle", "NO KA 'OI", "Barn's", "Clark's Botanicals", "Lana's Shop", "Lovin' Summer", \
                       "It's A 10", "Not Your Mother's", "KOHL'S", "Dillard's", "Francesca's", "L'Academie"]
    
    #brands with : , need to be different from ordinay
    special_brand3 = ['ralph lauren: polo', 'ralph lauren: lauren', 'ralph lauren: ralph', 'johan by: j.lindeberg', 'jl by: j.lindeberg', 'V::room', 'Werkstatt:Munchen', 'Nude:Masahiko Maruyama', 'Nude:mm', 'H:ours']
    
    
    for s in special_brands or special_brands2 or special_brand3:
        if s in text:
            brands.append(s)
            
    brand_found = []
    for b in brands:
        if b in text:
            brand_found.append(b)

    #print("with special case brands")
    #print(brand_found)
    return brand_found


#  get rid of space betweeen brand, extremely important in create/search in map
def find_all_brands(text):
    brands = []   
    brand_look_up_map={}
    
    # brands with special cases 
    b2 = find_brands_with_specialcase(text)

    for b in b2:

        #LOGIC : used to clean the special case brands_name
        nb = pre_clean_text_brands(b).replace(' ', '').lower()
        brands.append(nb)
        brand_look_up_map[nb] = upper_dict(brand_dict)[b.capitalize()]
        text = text.replace(b, nb)

    clean_text = pre_clean_text(text)

    b1 = find_brands_without_punc(clean_text)
    t = clean_text.lower()

    for b in b1:
        nb = b.replace(' ','').lower()
        brands.append(nb)
        if b in upper_dict(brand_dict).keys():
            brand_look_up_map[nb] = upper_dict(brand_dict)[b]
        else:
            pass
        t = t.replace(b.lower(), nb)

    return brands, t, brand_look_up_map

# check the occurance of duplicate item 
def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
            
    return locs  
  
# create the map of each brand and its postion in text
def create_brand_idx_map(text, brands):

    brand_idx_map = {}

    words = text.split(' ')

    for brand in brands:
        if brand in words:
            idx=list_duplicates_of(words, brand)
            for id in idx:
                brand_idx_map[id] = brand

    return brand_idx_map

# map brand to their original form 
def brand_idx_map_helper(brand_map, lookup_map):
    
    for key,value in brand_map.items():
        brand_map[key]= lookup_map[value]
        
    return brand_map



