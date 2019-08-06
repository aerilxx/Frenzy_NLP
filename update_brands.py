#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 14:48:20 2019

@author: bingqingxie
"""
import pymysql
import pymysql.cursors

'''
purpose of this file: 
replace brand name synomous in text with correct brand name
'''

#create dictionary for brand synomous
def create_brand_dictionary():
    brand_dict = {}
    
    conn = pymysql.connect(host='localhost',
                             user='root',
                             port = 8889,
                             passwd='root',
                             db='mpdb')
    
    try:
        with conn.cursor() as cursor:
            sql = "select s.brand, s.brand_id, b.brandname \
                from BrandSynomous as s \
                join brands as b \
                on b.id=s.brand_id"
            
            cursor.execute(sql)
            row = cursor.fetchone()
            while row is not None:
                brand_dict[row[0].lower()] = row[2].lower()
                row = cursor.fetchone()
                
   
    finally:
        conn.close()
        
    brand_dict2 = create_brandname_dictionary()
    brand_dict.update(brand_dict2)
        
    return brand_dict

# create brands list where key value is equal
def create_brandname_dictionary():
    brand_dict = {}
    
    conn = pymysql.connect(host='localhost',
                             user='root',
                             port = 8889,
                             passwd='root',
                             db='mpdb')
    
    try:
        with conn.cursor() as cursor:
            sql = " SELECT brandname AS old_brand, brandname AS new_brand FROM brands"
            
            cursor.execute(sql)
            row = cursor.fetchone()
            while row is not None:
                brand_dict[row[0]] = row[1]
                row = cursor.fetchone()
                
    finally:
        conn.close()
        
    return brand_dict



def brand_lemmerization(brand, brand_dict):
    
    clean_brand = str(brand).lower()
    if clean_brand in brand_dict:
        return brand_dict[brand]
    else:
        return brand

brand_dict1 = create_brand_dictionary() 
brand_dict2 = create_brandname_dictionary()
brand_dict1.update(brand_dict2)

# update brand dictionary everytime change 
with open('brands.txt', 'w') as file:
    file.write(str(brand_dict1))



        
        
        