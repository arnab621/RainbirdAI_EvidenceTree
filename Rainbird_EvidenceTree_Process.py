#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:53:28 2018

@author: arnab
"""

answerFactID = []
#function to yield a dictionary from a another dictionary
def find(key, dictionary, param):
    #for k, v in dictionary.iteritems(): #Python 2
    for k, v in dictionary.items():
        if k == key:
            if param in v:
                #print dictionary
                #yield dictionary
                yield v
        elif isinstance(v, dict):
            for result in find(key, v, param):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find(key, d, param):
                        yield result
                    
def find2(key, dictionary, param):
    #for k, v in dictionary.iteritems(): #Python 2
    for k, v in dictionary.items():
        if k == key:
            if param in v:
                if v not in answerFactID:
                    answerFactID.append(v)
                    
                    yield dictionary
                #else:
                #    yield {}
        elif isinstance(v, dict):
            for result in find2(key, v, param):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find2(key, d, param):
                        yield result
                    
                    
#list(find('factID', result, "RF"))

#Get all FactID with RF

KMID = "" #Enter the Knowledge Map ID
API = "" #Enter the API Key

url = "https://enterprise-api.rainbird.ai"

import requests, json
import pandas as pd
import os

proxy = '' #in case you have a proxy to bypass firewall etc.
os.environ['https_proxy'] = proxy

path="" #local file path
os.chdir(path)

factID = "" #the starting fact ID ..starts with WA:...

#r = requests.get(url+"/analysis/evidence/"+factID,auth=(API+":",""))
#result = r.json()

#ruleFactIDs = list(find('factID', result, "RF")) #get rule fact ID

ruleFactIDs = [factID]
#answerDicts = list(find2('factID', result, "AF"))# get dictionary of answer Facts
completedFacts = []
answerDicts = []
queryType = "RF" # this is where you need to capture what type of data (answer or rule) you are interested in
for factID in ruleFactIDs:
        
    r = requests.get(url+"/analysis/evidence/"+factID,auth=(API+":",""))
    result = r.json()
        
    completedFacts.append(factID)
    newruleFactIDs = list(find("factID", result, "RF"))
    if len(newruleFactIDs) > 1:
        for v in newruleFactIDs:
            if v not in completedFacts:
                if v not in ruleFactIDs:
                    ruleFactIDs.append(v)
                    
    newanswerDicts = list(find2('factID', result, queryType))
    #print len(newanswerDicts)
    for i in range(0,len(newanswerDicts)):
        answerDicts.append(newanswerDicts[i])


df = pd.DataFrame(answerDicts)
writer = pd.ExcelWriter('Rainbird_Evidence_Log.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()




