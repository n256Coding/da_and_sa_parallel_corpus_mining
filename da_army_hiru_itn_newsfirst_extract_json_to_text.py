#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 08:28:02 2022

@author: aloka
extract the json file content (news content) into a text file in the folder structure yy/mm/dd/text
input - json
output - textfile in y/m/d folder structure

"""
import json
import os
import nltk
from nltk.tokenize import sent_tokenize
import traceback

#nltk.download('punkt')

months_tamil=['ஜனவரி','பிப்ரவரி','மார்ச்','ஏப்ரல்','மே','ஜூன்','ஜூலை','ஆகஸ்ட்','செப்டம்பர்','அக்டோபர்','நவம்பர்','டிசம்பர்']
months_english=['January','February','March','April','May','June','July','August','September','October','November','December']
months_sinhala=['ජනවාරි','පෙබරවාරි','මාර්තු','අප්‍රේල්','මැයි','ජූනි','ජූලි','අගෝස්තු','සැප්තැම්බර්','ඔක්තෝබර්','නොවැම්බර්','දෙසැම්බර්']
month_arr=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#special chars & digits
digits_spChars={'1', '2','3','4','5','6','7','8','9','0','[',']','{','}','(',')','\\','/','=',';','-',',','|','.','+','*','x'}

#json file directory
root_path='/content/data/json_files'
sources=['hiru', 'newsfirst', 'itn'] #
langs=['english', 'sinhala', 'tamil']

#textfile path

text_file_path='/content/data/textfiles'

#check validity of sentence
def isvalid(sent):
    sent_chars=list(sent)
    sp_chars=digits_spChars.intersection(set(sent_chars))
    spChar_percentage=len(sp_chars)/len(sent_chars)*100
    print(spChar_percentage)

#clean sinhala sentence
def clean_sent(sent):
    sent=sent.replace(' ‍', '(')
    text_tokens=[token.strip() for token in sent.split()]
    mod_sent=' '.join(text_tokens)
    
    return mod_sent

#sentence extraction by tokenizing
def extract_sentences(sent_list):
    extracted_sentences=[]
    
    for sent in sent_list:                
        if len(sent.split()) !=0:
            sent=clean_sent(sent)
            if sent !='':
                extracted_sentences.append(sent)
    
    return extracted_sentences

#returns the sentences from json for itn news
def get_content_itn(json_file_path, file):    
    with open(json_file_path+'/'+file, 'r') as news_file:
        data=json.load(news_file)
        
        news_data=data['Content']
        
        sents=[]
        if isinstance(news_data, str):
            sentTkns=sent_tokenize(news_data)
            sents=[]
            
        else:
            sents=extract_sentences(news_data)        
        
        time_tokens=[t.strip() for t in data['Time'].strip().split()] #itn "\nඅගෝස්තු 10, 2018 11:03 "
        # ["\n01 Apr, 2020\t", "| 11:46 am ", "\n"]
        return time_tokens, sents
        
#returns the sentences from json for newsfirst news
def get_content_newsfirst(json_file_path, file,lang):    
    with open(json_file_path+'/'+file, 'r') as news_file:
        data=json.load(news_file)
        
        if lang=='tamil':
            news_data=data['Content'][1:]
        else:
            news_data=data['Content']
        
        sents=[]
        if isinstance(news_data, str):
            sents=sent_tokenize(news_data)
        else:
            sents=extract_sentences(news_data)        
        
        #"Time": ["\n01 Apr, 2020\t", "| 11:46 am ", "\n"]

        time=data['Time'][0].strip().split()
        day=time[0].strip()
        month=time[1].strip()[:-1]
        year=time[2].strip()        
        
        return day, month, year, sents   
    
#returns the sentences from json for army news
def get_content_army(json_file_path, file):    
    #time='15th July 2019 14:59:37 Hours' #army format
    #si - "Time": "07th February 2020 08:50:18 Hours"
    #ta - "Time": "05th July 2018 11:50:32 Hours"
    with open(json_file_path+'/'+file, 'r') as news_file:
        data=json.load(news_file)
        
        news_data=data['Content'][1:]
        
        sents=[]
        if isinstance(news_data, str):
            sents=sent_tokenize(news_data)
        else:
            sents=extract_sentences(news_data)        
        
        timeTkns=data['Time'].strip().split()
        day=timeTkns[0].strip()[:-2]
        month=month_arr[months_english.index(timeTkns[1])]
        year=timeTkns[2]    
        
        return day, month, year, sents 

#returns the sentences from json for army news
def get_content_hiru(json_file_path, file, lang):    
    #time_hiru="Wednesday, 02 October 2013 - 8:14" 
    #hiru si-"Tuesday, 02 July 2013 - 10:03" 
    #hiru ta-"Wednesday, 02 October 2013 - 20:12"
    
    # en - "Time": "Friday, 02 January 2015 - 8:01"
    # si - "Time": "Friday, 02 January 2015 - 7:43"
    # ta - "Time": "Friday, 02 January 2015 - 8:56"
    
    with open(json_file_path+'/'+file, 'r') as news_file:
        data=json.load(news_file)
        
        if lang=='sinhala':
            news_data=data['Content'][:-2]
        else:
            news_data=data['Content']#[:-2] ignore last two
        
        sents=[]
        if isinstance(news_data, str):
            sents=sent_tokenize(news_data)
        else:
            sents=extract_sentences(news_data)        
        
        timeTkns=data['Time'].strip().split()

        day=timeTkns[1].strip()
        month=month_arr[months_english.index(timeTkns[2])]
        year=timeTkns[3]   
        
        return day, month, year, sents 

summary_file_counts=[]
count_dummy=0

for source in sources:

    for lang in langs:
        
        json_file_path=root_path+'/'+source+'/'+lang
        json_files=os.listdir(json_file_path)
        
        file_count=0
        
        for json_file in json_files:    
            try:                
                
                year=''
                month=''
                day=''
                sentences=[]
                
                if source=='itn':
                    time_tokens, sentences=get_content_itn(json_file_path, json_file)      
                    
                    #get yy/mm/dd
                    year=int(time_tokens[2])
                    day=time_tokens[1][:-1]
                    if lang=='english':
                        month=month_arr[months_english.index(time_tokens[0])]
                    elif lang=='sinhala':
                        month=month_arr[months_sinhala.index(time_tokens[0])]
                    elif lang=='tamil':
                        month=month_arr[months_tamil.index(time_tokens[0])]
                        
                elif source=='newsfirst':
                    day, month, year, sentences =get_content_newsfirst(json_file_path, json_file,lang)  
                elif source=='hiru':
                    day, month, year, sentences =get_content_hiru(json_file_path, json_file, lang) 
                elif source=='army':
                    day, month, year, sentences =get_content_army(json_file_path, json_file)             
                
                
                text_file_name=json_file.strip().split()[-1]
                text_file_date_dir=text_file_path+'/'+source+'/'+lang+'/'+str(year)+'/'+month+'/'+day    
                                      
                try:
                    os.makedirs(text_file_date_dir)
                except:
                    count_dummy+=1
                    #print('dir exists')
                       
                fileOut=open(text_file_date_dir+'/'+text_file_name.replace('json', 'txt'), 'w', encoding='utf8')
                
                
                for sent in sentences:
                    fileOut.write('{}\n'.format(sent))
                fileOut.close()
                file_count+=1

            except Exception as e:
                traceback.print_exc()
                print('ERROR: {}/{}'.format(json_file_path, json_file)) 
                break
                
        #print('{} files : {}'.format(lang, file_count))
        summary_file_counts.append('{}-{} [json/txt][error files] : {}/{}[{}]'.format(source, lang, len(json_files), file_count, (len(json_files)-file_count)))

print('########################################################################################################################')
print('Summary:')
print('########################################################################################################################')

for item in summary_file_counts:
    print(item)

        
                    
        



