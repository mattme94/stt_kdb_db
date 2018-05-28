# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 20:06:27 2018

@author: mepcr
"""
from lxml import etree, objectify, html
import jinja2 
import os
import requests
import re
from collections import OrderedDict
import math

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

def statsparse(link, dic, name, ID):
    character = requests.get(link)
    ctree = html.fromstring(character.content)
    
    s=ctree.xpath('//span[@id="Away_Team_Skills"]/../following-sibling::p')
    skills=OrderedDict.fromkeys(s[0].xpath('a/@title')[1:][:-1]).keys()   
    table=ctree.xpath('//span[@id="Away_Team_Skills"]/../following-sibling::table')
    results=[]
    for rows in table[0].xpath('tr'):
        table_data=rows.xpath('td')
        if table_data:
            results.append([(data.text_content()).encode('ascii','replace').strip().split('Avg')[0].split('?') for data in table_data])
            
    for i,x in enumerate(results):
        if not "" in results[i][0]:
            for j in range(1, len(results[i])):     
                if not "" in results[i][j]:
                    dic['ID'].append(ID)
                    dic['name'].append(name)
                    dic['levels'].append(results[i][0][0])
                    dic['stars'].append(str(math.ceil((float(j)/float(len(skills))))))
                    dic['skill'].append(skills[(j-1)%len(skills)])
                    dic['minv'].append(results[i][j][0])
                    dic['avg'].append(sum(int(c) for c in results[i][j])/2)
                    dic['maxv'].append(results[i][j][1])
    return dic


page = requests.get('https://stt.wiki/wiki/Crew/List')
tree = html.fromstring(page.content)

l=tree.xpath('//tr/td[@style="padding:0px;"]/..')

name=[]
base=[]
link=[]
rarity=[]
traits=[]
skills=[]

dic={}
dic['name']=[]
dic['levels']=[]
dic['stars']=[]
dic['skill']=[]
dic['minv']=[]
dic['avg']=[]
dic['maxv']=[]
dic['ID']=[]

ID=1
for i in range(0, len(l)):
    print i
    temp=[]
    t=l[i].xpath('td[@style="padding:0px;"]/a/@title')[0].replace('"',"'")
    name.append(t) #Variant Name
    print (name[i])
    base.append(l[i].xpath('td[@style="padding:0px; width:10em;"]/a/@title')[0]) #Base CHaracter
    link.append('https://stt.wiki'+l[i].xpath('td[@style="padding:0px;"]/a/@href')[0])#Link to page
    rarity.append(l[i].xpath('td[@style="padding:0px; width:10em;"]/following-sibling::td[1]/span/img/@alt')[0])#Rarity
    for j in range (2, 8):
        t=l[ i].xpath('td[@style="padding:0px; width:10em;"]/following-sibling::td['+str(j)+']/a/@title')
        if len(t)>0:
            temp.append(str(t[0]))
    skills.append(temp)
    temp=[]
    t=l[i].xpath('following-sibling::tr[@class="expand-child"][1]/td[@colspan]/a/text()')
    for x in t:
        temp.append(str((re.sub(r'[^\x00-\x7F]+','', x))))
    traits.append(temp)#Traits
    print ("Finding Stats")
    dic=statsparse(link[i],dic,name[i],i)

    
c={'name':name,'base':base,'link':link,'rarity':rarity,'skills':skills,'traits':traits, 'name_long':dic['name'],'levels_long':dic['levels'],'stars_long':dic['stars'],'skill_long':dic['skill'],'min_long':dic['minv'],'avg_long': dic['avg'],'max_long':dic['maxv'],'ID':dic['ID']}


result=render('db.template', c)

with open("db.q", "wb") as fh:
   fh.write(result)

