# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 22:47:54 2018

@author: mepcr
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

# share spreadsheet with stt-958@lateral-name-194904.iam.gserviceaccount.com
 
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name("My Project-2e928866c033.json", scope)
client = gspread.authorize(creds)
 
# Make sure you use the right name here.
spreadsheet = client.open("StarTrek Timelines-Stats")
sheets=[x.title for x in spreadsheet.worksheets()]
items={}
dfs={}
rarity_list=['Basic','Common','Uncommon','Rare','Super Rare']
level_defs={'1':'Normal','2':'Elite','3':'Epic'}



for i in range (1, len(sheets)):
    print(sheets[i])
    ws=spreadsheet.worksheet(sheets[i])
    df = pandas.DataFrame(ws.get_all_values())
    df.columns=df.iloc[0]
    df.reindex(df.index.drop(0))
    columns=df.columns.tolist()
    df.rename(columns={ df.columns[len(columns)-1]: "Warp" }, inplace=True)
    cols=[x for x in df.columns.tolist() if x!='Index']
    df[cols] = df[cols].apply(pandas.to_numeric, errors='coerce')
    dfs[sheets[i]]=df

    item_list=[x.encode('ascii','replace').replace('?',' ').strip() for x in cols[:-1]]
    item_listraw=[x for x in cols[:-1]]
    warp_count=sum(df['Warp'].fillna(1))
    
    for index,gear in enumerate(item_list):
        rarity=[y for y in rarity_list if y in gear]
        if len(rarity)==0:
            rarity=""
        else:
            rarity=rarity[-1]
            gear=gear.split(rarity)[-1].strip()
        if gear == "Summary!A1":
                ws.update_acell('A1',ws.acell('A1').input_value.replace('"Summary!A1"','"Index"'))
        if rarity!="":
            if not gear in items:
                items[gear]={rarity:pandas.DataFrame()}
            if rarity not in items[gear]:
                items[gear][rarity]=pandas.DataFrame()
            items[gear][rarity]=items[gear][rarity].append({'Mission':sheets[i],'Count':sum(df[item_listraw[index]].fillna(0)),'Warp':warp_count, 'Ratio':sum(df[item_listraw[index]].fillna(0))/warp_count}, ignore_index=True)
        else:
            if not gear in items:
                items[gear]=pandas.DataFrame()
            items[gear]=items[gear].append({'Mission':sheets[i],'Count':sum(df[item_listraw[index]].fillna(0)),'Warp':warp_count, 'Ratio':sum(df[item_listraw[index]].fillna(0))/warp_count}, ignore_index=True)


def excelread(sheetname):
    excel=pandas.ExcelFile(sheetname)
    
    sheets=excel.sheet_names
    items={}
    dfs={}
    
    for i in range(1, len(sheets)):
        df=excel.parse(sheets[i])
        columns=df.columns.tolist()
        df.rename(columns={ df.columns[len(columns)-1]: "Warp" }, inplace=True)
        dfs[sheets[i]]=df
        
        item_list=[x.encode('ascii','replace').replace('?',' ').strip() for x in (df.columns.tolist())[1:][:-1]]
        item_listraw=[x for x in (df.columns.tolist())[1:][:-1]]
        warp_count=sum(df['Warp'].fillna(1))
        
        for j,x in enumerate(item_list):
            if not x in items:
                items[x]=pandas.DataFrame()
            items[x]=items[x].append({'Mission':sheets[i],'Count':sum(df[item_listraw[j]].fillna(0)),'Warp':warp_count, 'Ratio':sum(df[item_listraw[j]].fillna(0))/warp_count}, ignore_index=True)
 
    
itemName=[]
itemRarity=[]
missionName_item=[]
missionLevel_item=[]
runsDone=[]  
itemReturn=[]  
itemPerRun=[]
itemId=[]
Id=1
for gear in items:
    if type(items[gear])==dict:
        for rarity in items[gear]:
            for row in range(0,len(items[gear][rarity])):
                itemId.append(Id)
                itemName.append(gear)
                itemRarity.append(rarity)
                runsDone.append(items[gear][rarity].loc[row,'Warp'])
                itemReturn.append(items[gear][rarity].loc[row,'Count'])
                if items[gear][rarity].loc[row,'Warp']==0:               
                    itemPerRun.append(0)
                else:
                    itemPerRun.append(items[gear][rarity].loc[row,'Count']/items[gear][rarity].loc[row,'Warp'])
                missionName_item.append(items[gear][rarity].loc[row,'Mission'].rsplit('-',1)[0].strip())
                missionLevel_item.append(level_defs[items[gear][rarity].loc[row,'Mission'].rsplit('-',1)[1].strip()])
            Id+=1
    else:
        for row in range(0,len(items[gear])):
            itemId.append(Id)
            itemName.append(gear)
            itemRarity.append('')
            runsDone.append(items[gear].loc[row,'Warp'])
            itemReturn.append(items[gear].loc[row,'Count'])
            if items[gear].loc[row,'Warp']==0:
                itemPerRun.append(0)
            else:
                itemPerRun.append(items[gear].loc[row,'Count']/items[gear].loc[row,'Warp'])
            missionName_item.append(items[gear].loc[row,'Mission'].rsplit('-',1)[0].strip())
            missionLevel_item.append(level_defs[items[gear].loc[row,'Mission'].rsplit('-',1)[1].strip()])
        Id+=1
        

c={'itemId':itemId,'itemName':itemName,'itemRarity':itemRarity,'runsDone':runsDone,'itemReturn':itemReturn,'itemPerRun':itemPerRun,'missionName':missionName_item,'missionLevel':missionLevel_item}

result=render('ItemList.template', c)

with open("ItemList.q", "wb") as fh:
   fh.write(result)    