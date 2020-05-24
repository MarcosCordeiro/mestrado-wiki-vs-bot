#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install numpy
#!pip install --user -U nltk
#nltk.download('stopwords')
#nltk.download('punkt')
#!pip install unidecode
#!pip install matplotlib
#!pip install pyhive


# In[2]:


import pandas as pd
import nltk
import time
import datetime
import boto3
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import RSLPStemmer
from unidecode import unidecode
from pyhive import hive


# In[3]:


#Carrega dados refined do Hive
df = pd.read_csv("defined.csv", names=["wiki_id", "title", "timestamp", "user","bot"])
#host="ec2-34-230-59-24.compute-1.amazonaws.com"
#conn = hive.Connection(host=host,port= 10000)
#dataframe = pd.read_sql("SELECT wiki_id, title, wiki_timestamp, wiki_user, bot FROM defined.wikidata", conn)


# ## Parte 1
# ## Pré Processamento

# In[4]:


#Remove linhas com dados nulos, transformando em minusculo e removendo aspas simples
df.dropna(inplace=True)
df["user"] = df["user"].replace({'\'': ''}, regex=True)
lw_text = df["title"].str.lower()
lw_text = lw_text.replace({'\'': ''}, regex=True)
df["user"] = df["user"].str.strip().replace({'^[0-9]*$': 'unknown'}, regex=True)


# In[5]:


#Normalizando timestamp
s = "01/01/2020"
default_timestamp = int(datetime.datetime.strptime('01/01/2020', '%d/%m/%Y').strftime("%s"))
df["timestamp"] = df["timestamp"].str.strip().replace({'^((?![0-9]).)*$': default_timestamp}, regex=True)


# In[6]:


#Substitui valores diferentes de booleano pela item de maior frequencia
max_freq = df.bot.mode()[0]
df["bot"] = df["bot"].str.strip().replace({'^((?!(False|True)).)*$': max_freq.strip()}, regex=True)
#df["bot"] = df["bot"].astype(bool)


# In[7]:


#Cria os tokens dos titulos
tokens =  lw_text.apply(word_tokenize)


# In[8]:


#Normalizando com unicode
tokens_uni = tokens.apply(lambda x: [unidecode(z) for z in x ])


# In[9]:


#Remove stopwords
stopwords = nltk.corpus.stopwords.words('portuguese')
stopwords.extend(['categoria','artigos', 'predefinicao','ficheiro','sobre','predefinicoes','redirecionamentos','esbocos','ligados','elemento','inexistentes','ficheiros','usuario','wikidata','paginas','wikipedia','discussao','lista'])
stopwords = set(stopwords + list(punctuation))
title_cleaned = tokens_uni.apply(lambda line:  [w for w in line if not w in stopwords])


# In[10]:


#Cria coluna com os titulos tratados
df["title_cleaned"] = title_cleaned.apply(lambda line: " ".join(line))
df.replace("", np.nan, inplace=True)
df.dropna(inplace=True)
df.head()


# In[11]:


#Cria coluna com os titulos com steamming
def Stemming(sentence):
    stemmer = RSLPStemmer()
    phrase = []
    for word in sentence:
        phrase.append(stemmer.stem(word.lower()))
    return phrase

stemmed_list = title_cleaned.apply(lambda line: Stemming(line))
df["title_stemmed"] = stemmed_list.apply(lambda line: " ".join(line))
df.head()


# ### DynamoDB

# In[13]:


# Grava tabela tratada no DynamoDB
MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''

resource = boto3.resource('dynamodb', aws_access_key_id=MY_ACCESS_KEY_ID, aws_secret_access_key=MY_SECRET_ACCESS_KEY, region_name='us-east-1')

df2 = df
for i in df2.columns:
    df2[i] = df2[i].astype(str)

myl=df2.T.to_dict().values()

table = resource.Table('wikibot-title_cleaned')
i =0
for w in myl:
    i=i+1
    table.put_item(Item=w)
    
print("Iten(s) gravado(s) " + str(i))


# In[ ]:




