# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 18:26:52 2018

@author: mepcr
"""

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

page = requests.get('https://stt.wiki/wiki/Missions')
tree = html.fromstring(page.content)

level_defs={0:'Normal',1:'Elite',2:'Epic'}

mission_number={}
mission_title={}
mission_type={}
mission_cost={}
mission_credits={}

missionName=[]
missionRarity=[]
missionType=[]
missionCost=[]
missionLocationFull=[]
missionLocationShort=[]
missionId=[]
ID=1

epis_1=[y for y in (x for x in tree.xpath('//h3/span') if str == type(x.text)) if 'Episode' in y.text]
epis_2=[y for y in (x for x in tree.xpath('//h3/span/a') if str == type(x.text)) if 'Episode' in y.text]
distress=[y for y in (x for x in tree.xpath('//h3/span/a') if str == type(x.text)) if 'Distress' in y.text]
cadet=tree.xpath('//h2/span[@id="Cadet_Challenges"]/../following-sibling::h3/span/a')

episodes=epis_1+epis_2+distress+cadet
episodes_name=[x.text.split('-')[-1].strip() for x in episodes]

for index,html_object in enumerate(episodes):
    mission_number[episodes_name[index]]=[x.text.split(' ')[-1] for x in html_object.xpath('../../following-sibling::table[1]/tr/td[not(@colspan)]/b') if 'Mission' in x.text]
    mission_title[episodes_name[index]]=[x.text for x in html_object.xpath('../../following-sibling::table[1]/tr/td[not(@colspan)]/b/following-sibling::a[1]')]
    mission_type[episodes_name[index]]=html_object.xpath('../../following-sibling::table[1]/tr/td[not(@colspan)]/b/../following-sibling::td[1]/a/@title')
    mission_cost[episodes_name[index]]=[x.text.encode('ascii','replace').replace('?','').strip().split('|') for x in html_object.xpath('../../following-sibling::table[1]/tr/td[not(@colspan)]/b/../following-sibling::td[2]')]
    mission_credits[episodes_name[index]]=[x.text.encode('ascii','replace').replace('?','').strip().split('|') for x in html_object.xpath('../../following-sibling::table[1]/tr/td[not(@colspan)]/b/../following-sibling::td[6]')]

for index,episode in enumerate(mission_number):
    for mission in range(0, len(mission_credits[episode])):
        for level in range(0, len(mission_credits[episode][mission])):
            missionName.append(mission_title[episode][mission])
            missionRarity.append(level_defs[level])
            missionType.append(mission_type[episode][mission])
            if len(mission_cost[episode][mission])==1:
                missionCost.append(mission_cost[episode][mission][0])
            else:
                missionCost.append(mission_cost[episode][mission][level])
            missionLocationFull.append(episode+'-'+mission_number[episode][mission])
            missionLocationShort.append(str(index+1)+'-'+mission_number[episode][mission])
            missionId.append(ID)
            ID+=1


c={'missionName':missionName,'missionRarity':missionRarity,'missionType':missionType,'missionCost':missionCost,'missionLocationFull':missionLocationFull,'missionLocationShort':missionLocationShort,'missionId':missionId}

result=render('mission.template', c)

with open("mission.q", "wb") as fh:
   fh.write(result)


