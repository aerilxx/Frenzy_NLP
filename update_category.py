#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 17:53:42 2019

@author: bingqingxie
"""
'''
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from gsheets import Sheets


# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('frenzynlp-client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.

#category_pair = client.open("key_pair_category").sheet2
#exception_pair = client.open("key_pair_category").sheet3

#'Spreadsheet'
key_pair = client.open("test").sheet1
#worksheet
#ws = key_pair.worksheet('Sheet1')
key_pair.to_csv('Spam.csv', encoding='utf-8', dialect='excel')




def create_category_pair():
    key_pair = client.open("key_pair_category").sheet1
    keyword = key_pair.col_values(1)
    category_detail_dict = {}
    key = ''
    cat_list= []

    for i in range(2,len(keyword)):
        
        each_row=key_pair.row_values(i)
    
        descriptive_category = each_row[0].split(',')
        main_category = each_row[1].split(',')
        value = each_row[2]
        
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
    product_rule_exception = client.open("key_pair_category").sheet3
    
     
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




print(type(keyword))

'''














