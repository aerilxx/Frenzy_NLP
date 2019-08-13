#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 13:07:12 2019
fdffdsf
@author: bingqingxie
"""

from bs4 import BeautifulSoup
import urllib
import urllib.request
from urllib.error import HTTPError
import re
import random
import json

def deEmojify(inputString):
   return inputString.encode('ascii', 'ignore').decode('ascii')

def get_user_agent():
    proxies = [
        "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
        "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0"]
    idx = random.randrange(0, len(proxies))
    return proxies[idx]


def cleanme(soup):
    for script in soup(["script"]):
        script.extract()

    return soup

# used to collect all avoided sections in the page
def remove_comments(content):
    avoid_text = content.find_all('div', 'comment-box')
    avoid1_text = content.find_all('footer')
    avoid2_text = content.find_all('ol', 'commentlist')
    avoid3_text = content.find_all('div', 'comment-respond')
    avoid4_text = content.find_all('div', 'post-comments')
    avoid5_text = content.find_all('div', 'comments')

    # this case fix “http://houseofmarz.com/2018/12/18/wrapped-up-in-white-faux-fur-2/#more-5141#comments” to exclude the comment
    avoidlist = []
    for a in avoid_text:
        avoidlist.extend(a.find_all('p'))
    for a in avoid1_text:
        avoidlist.extend(a.find_all('p'))
    for a in avoid2_text:
        avoidlist.extend(a.find_all('p'))
    for a in avoid3_text:
        avoidlist.extend(a.find_all('p'))
    for a in avoid4_text:
        avoidlist.extend(a.find_all('p'))
    for a in avoid5_text:
        avoidlist.extend(a.find_all('p'))

    return avoidlist

# used to
# 1) collect data from that div inlcuding data which is not inside any tags
# 2) adding or removing data from other tags like p, h1-6, td, span and avoidlist
def clean_divs(content, avoidlist):

    final = content.get_text(separator=' ')  # following 3 lines to get the code outside of p, h1-6, span, td
    # final = content.get_text()  # following 3 lines to get the code outside of p, h1-6, span, td
    ending = ['!', '?', ',', '=', '-', '+', '/', '|', '.', '~']        # list used to check whether sentence ends with this list or not. and if not append a dot
    sent = final.split('\n')
    for i in range(len(sent)):
        while len(sent[i]) > 0 and sent[i][-1] == ' ':
            sent[i] = sent[i][0:-1]
        if len(sent[i]) > 0 and sent[i][-1] not in ending:
             sent[i] = sent[i] + ' .\n'


    final = ''.join(sent)
    res = []
    for word in list(final.split(' ')):
        if len(word) > 0:
            res.append(word)

    final = ' '.join(res)
    buffer_text = ''
    # print("Final")
    # print(final)
    # print("********************************************************************")
    for paragraph in content.find_all(['p', re.compile("^h[1-6]$"), "td", "span" ,"img", "a"]):
        if paragraph not in avoidlist:
            # logic : this if-else code is added at last, if any bugs comes, remove this logic
            # logic is to combine multiple span tags into one text by iterating them and adding to buffer, as soon as new different tag arrives append the bufffer_text into main text
            if paragraph.name == "span":
                if paragraph.string is not None:
                    text_to_add = paragraph.string.encode('utf-8').decode('utf-8')
                    # logic : sometimes string may end with special characters like \n,\t , so to avoid it
                    if text_to_add[0:-1] not in final:
                        buffer_text = buffer_text + ' ' + text_to_add
                else:
                    text_to_add = paragraph.get_text()
                    # logic : sometimes string may end with special characters like \n,\t , so to avoid it
                    if text_to_add[0:-1] not in final:
                        buffer_text = buffer_text + ' ' + text_to_add
                continue
            else:
                final = final + '.\n' + buffer_text
                if len(buffer_text) > 0 and buffer_text[-1] not in ending:
                    final = final + ' .\n'
                buffer_text = ''

                if paragraph.name == "img" or paragraph.name == "a":
                    continue

            if paragraph.string is not None:
                check = paragraph.string.encode('utf-8').decode('utf-8').strip()
                res = []
                for word in list(check.split(' ')):
                    if len(word) > 0:
                        res.append(word)

                check = ' '.join(res)
                # logic : sometimes string may end with special characters like \n,\t , so to avoid it
                if len(check)>1 and check[1:-2] not in final:  # site: http://fashionmixbag.blogspot.com/
                    print("paragrpah string", type(check), check)

                    final = final + '\n' + check
                    if check[-1] not in ending:
                        final = final + ' .'

            # elif paragraph.get_text is not None and str(paragraph.get_text()) not in check_final:
            elif paragraph.get_text(separator=' ') is not None:
                check = paragraph.get_text(separator=' ')
                sent = check.split('\n')
                for check in sent:
                    # sometimes get_text() returns multiple line, so we loop over all the lines in it.c
                    res = []
                    for word in list(check.split(' ')):
                        if len(word) > 0:
                            res.append(word)

                    check = ' '.join(res)
                    # logic : sometimes string may end with special characters like \n,\t , so to avoid it
                    if len(check)>1 and check[1:-2] not in final:
                        print("Paragrpah get_text", type(check), check)
                        final = final + '\n' + check
                        if check[-1] not in ending:
                            final = final + ' .'
    return final

# used to avoid all comments and other text from artcile and soup
def clean_art_soup(content, avoidlist):
    text = ''
    buffer_text = ''
    # removed ')' from ending
    ending = ['!', '?', ',', '=', '-', '+', '/', '|', '.', '~']
    for paragraph in content.find_all(['p', re.compile("^h[1-6]$"), "td", "span", "img", "a"]):
        if paragraph not in avoidlist:
            # logic : this if-else code is added at last, if any bugs comes, remove this logic
            # logic is to combine multiple span tags into one text by iterating them and adding to buffer, as soon as new different tag arrives append the bufffer_text into main text
            if paragraph.name == "span":
                if paragraph.string is not None:
                    text_to_add = paragraph.string.encode('utf-8').decode('utf-8')
                    # logic : sometimes string may end with special characters like \n,\t , so to avoid it
                    if text_to_add[0:-1] not in text:
                        buffer_text = buffer_text + ' ' + text_to_add
                else:
                    text_to_add = paragraph.get_text()
                    # logic : sometimes string may end with special characters like \n,\t , so to avoid it
                    if text_to_add[0:-1] not in text:
                        buffer_text = buffer_text + ' ' + text_to_add
                continue
            else:
                # print(buffer_text)
                text = text + '.\n' + buffer_text
                if len(buffer_text) > 0 and buffer_text[-1] not in ending:
                    text = text + ' .\n'
                buffer_text = ''

                if paragraph.name == "img" or paragraph.name == "a":
                    continue

            # print(paragraph)
            if paragraph.string is not None:
                text_to_add = paragraph.string.encode('utf-8').decode('utf-8')
                # logic : sometimes string may end with special characters like \n,\t , so to avoid it
                if text_to_add[0:-1] not in text:
                    text = text + ' .\n' + text_to_add.strip()
                    if len(text_to_add) > 0 and text_to_add[-1] not in ending:
                        text = text + ' .\n'
            else:
                text_to_add = paragraph.get_text()
                # logic : sometimes string may end with special characters like \n,\t , so to avoid it
                if text_to_add[0:-1] not in text:
                    text = text + ' .\n' + text_to_add.strip()
                    if len(text_to_add) > 0 and text_to_add[-1] not in ending:
                        text = text + ' .\n'

    return text

def crawl_text(link):
    agent = get_user_agent()
    # fix internal server on site “https://www.elizahiggins.com/happy-hot-and-sweaty-nyfw/”

    req = urllib.request.Request(link, headers={'User-Agent': agent})
    try:
        url = urllib.request.urlopen(req)
        s = url.read()

    except HTTPError as e:
        s = e.read()

    #soups = BeautifulSoup(s, 'html.parser')
    soups = BeautifulSoup(s, 'lxml')
    
    soup = cleanme(soups)
    content = soup.find('div', 'entry-content')
    content2 = soup.find('div', 'content')  # fixed a special case for site http://adletfashion.com/en/
    content3 = soup.find('div',
                         'post-content')  # added a special case for site :https://beckienye.com/2018/01/10/if-i-were-a-baker-boy/
    content4 = soup.find('div', 'storycontent')

    art = soup.find('article')  # fix post layout without entry-content but in article section

    final2 = ''
    final3=''
    final4=''
    text_art = ''

    flag = False

    if content is not None:
        print("Text in entry-content")

        avoidlist = remove_comments(content)
        flag = True
        check_final = clean_divs(content, avoidlist)
        final1 = ''.join(check_final)
        # print(type(final2))
        return final1


    if content2 is not None:
        print("Text in content")
        # final = content2.get_text()
        avoidlist = remove_comments(content2)
        flag = True
        check_final = clean_divs(content2, avoidlist)
        final2 = ''.join(check_final)

    if content3 is not None:
        print("Text in post-content")
        # final = content3.get_text()
        avoidlist = remove_comments(content3)
        flag = True
        check_final = clean_divs(content3, avoidlist)
        final3 = ''.join(check_final)

    if content4 is not None:
        print("Text in post-content")
        avoidlist = remove_comments(content4)
        flag = True
        check_final = clean_divs(content4, avoidlist)
        final4 = ''.join(check_final)

    if art is not None:
        print("Text in article")
        text = ''
        avoidlist = remove_comments(art)
        text_art = clean_art_soup(art, avoidlist)

    elif flag == False:
        print("Text in soup")
        avoidlist = remove_comments(soup)
        text = ''

        text = clean_art_soup(soup, avoidlist)
        return text

    # logic :
    #  sometimes text contains article tags and one of div-content tags too, sometimes it may be some line or comments so just added lines to return max_length of all

    li = [final2, final3, final4, text_art]
    return max(li, key=len)

############################################################################################################################################################################


# scrap imgs in script tag, usually in carousel
def crawl_img_from_javascript(soup):
    images = set()
    imgs = []
    #different websites have different patterns, change accordingly
    pattern = re.compile('var GALLERY_DATA = (.*?);$')
    
    scripts = soup.find_all('script')
    for script in scripts:
        if pattern.match(str(script.string)):
            data = pattern.match(str(script.string))
            imgs = json.loads(data.groups()[0])
            
    for img in imgs:
        images.add(img['src'][0])

    return images

def crawl_img(link):
    # set avoid duplicate
    images = set()
    agent = get_user_agent()
    # fix internal server on site "https://www.elizahiggins.com/happy-hot-and-sweaty-nyfw/"
    req = urllib.request.Request(link, headers={'User-Agent': agent})
    try:
        url = urllib.request.urlopen(req)
        s = url.read()

    except HTTPError as e:
        s = e.read()

    #soup = BeautifulSoup(s, 'html.parser')
    soup = BeautifulSoup(s, 'lxml')

    content = soup.find('div', 'entry-content')
    content2 = soup.find('div', 'storycontent')

    art = soup.find('article')

    # exclude plugin picture with these keywords
    avoid = ["facebook", "pinit", "instagram", "search", "google", "pinterest", "linkedin", "twitter", "sold", "loader","follow_subscribe"]

    carousel = crawl_img_from_javascript(soup)
    
    imgs = set()

    # case 1: html has entry-content
    if content is not None:
        imgs = content.find_all('img')

    elif content2 is not None:
        imgs = content2.find_all('img')

    elif art is not None:
        print('image have article tag')
        imgs = art.find_all('img')

    else:
        print("Content is none")
        imgs = soup.find_all('img')

    imagesnosize = set()
    
    for img in imgs:
        if img.has_attr('src'):
            flag = 0
            for a in avoid:
                if a in img['src']:
                    flag = 1
                    break
            if flag == 1:
                continue

            # exclude picutre size smaller than 350 pixle
            if img['src'] is not None and (img['src'].startswith('http') or img['src'].startswith('https')):
                # if img.has_attr('width') and isinstance(img['width'], int) and int(img['width']) < 350:          
                if img.has_attr('width'):
                    # logic : added tnis case to avoid % in img width
                    if img['width'][-1] == '%':
                        continue
                    elif int(img['width']) < 300:
                        continue
                    else:
                        images.add(img['src'])

                elif img.has_attr('sizes'):
                    # print((img['sizes'][img['sizes'].rfind(' ') + 1:img['sizes'].rfind('px')]) == "")
                    # print("(*8")
                    if (img['sizes'][img['sizes'].rfind(' ')+1 : img['sizes'].rfind('px')]) == "":
                        continue
                    #logic : This site failed for https://www.whowhatwear.com/how-to-live-a-stylish-life--5b4668b812320/slide2 if I do not write the above code
                    if (int(img['sizes'][img['sizes'].rfind(' ')+1 : img['sizes'].rfind('px')]) < 350):
                        continue
                    else:
                        images.add(img['src'])

                elif not img.has_attr('sizes') and not img.has_attr('width'):
                    imagesnosize.add(img['src'])
                    
            if img['src'] is not None and img['src'].endswith('gif'):
                images.add(img['data-src'])

    # in case all images in post have no size, scrap all imgs
    if len(images) == 0 and len(imagesnosize) >= 1:
        print("Image_no_size")
        return imagesnosize

    # added this case if all images are less than 350 width
    if len(images) == 0:
        for img in imgs:
            images.add(img['src'])

    # append images in carasoel     
    if carousel is not None:
        for img in carousel:
            print(img)
            images.add(img)
            
    return images



