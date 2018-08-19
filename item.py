# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 22:47:54 2018

@author: mepcr
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas

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
                print(sheets[i])
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
    
