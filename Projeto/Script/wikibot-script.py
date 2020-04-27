#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install -U scikit-learn
#!pip install numpy
#!pip install --user -U nltk
#nltk.download('stopwords')
#nltk.download('punkt')
#!pip install unidecode
#!pip install matplotlib


# In[1]:


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
from sklearn.feature_extraction.text import TfidfVectorizer


# In[2]:


#Carrega dados refined
df = pd.read_csv("../s3_data/refined/refined.csv", names=["wiki_id", "title", "timestamp", "user","bot"])


# ## Pré Processamento

# In[3]:


#Remove linhas com dados nulos, transformando em minusculo e removendo aspas simples
df["title"].dropna(inplace=True)
df["bot"].dropna(inplace=True)
df["user"] = df["user"].replace({'\'': ''}, regex=True)
lw_text = df["title"].str.lower()
lw_text = lw_text.replace({'\'': ''}, regex=True)
df["user"] = df["user"].str.strip().replace({'^[0-9]*$': 'unknown'}, regex=True)


# In[4]:


#Normalizando timestamp
s = "01/01/2020"
default_timestamp = int(datetime.datetime.strptime('01/01/2020', '%d/%m/%Y').strftime("%s"))
df["timestamp"] = df["timestamp"].str.strip().replace({'^((?![0-9]).)*$': default_timestamp}, regex=True)


# In[5]:


#Substitui valores diferentes de booleano pela item de maior frequencia
max_freq = df.bot.mode()[0]
df["bot"] = df["bot"].str.strip().replace({'^((?!(False|True)).)*$': max_freq.strip()}, regex=True)
#df["bot"] = df["bot"].astype(bool)


# In[6]:


#Cria os tokens dos titulos
tokens =  lw_text.apply(word_tokenize)


# In[7]:


#Normalizando com unicode
tokens_uni = tokens.apply(lambda x: [unidecode(z) for z in x ])


# In[8]:


#Remove stopwords
stopwords = nltk.corpus.stopwords.words('portuguese')
stopwords.extend(['categoria','artigos', 'predefinicao','ficheiro','sobre','predefinicoes','redirecionamentos','esbocos','ligados','elemento','inexistentes','ficheiros','usuario','wikidata','paginas','wikipedia','discussao','lista'])
stopwords = set(stopwords + list(punctuation))
title_cleaned = tokens_uni.apply(lambda line:  [w for w in line if not w in stopwords])


# In[9]:


#Cria coluna com os titulos tratados
df["title_cleaned"] = title_cleaned.apply(lambda line: " ".join(line))
df.replace("", np.nan, inplace=True)
df.dropna(inplace=True)
df.head()


# In[10]:


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


# In[11]:


# Separa dataframes entre bots true e false
title_bot_true = df[(df.bot == 'True')][["title","title_cleaned","title_stemmed"]]
title_bot_true.head()


# In[12]:


title_bot_false = df[(df.bot == 'False')][["title","title_cleaned","title_stemmed"]]
title_bot_false.head()


# In[13]:


# Vec. transform com bots = true
str_list = title_bot_true["title_stemmed"].values
vec = TfidfVectorizer()
vec.fit(str_list)
features_bot_true = vec.transform(str_list)
print(features_bot_true)

# In[14]:


# Vec. transform com bots = false
str_list = title_bot_false["title_stemmed"].values
vec.fit(str_list)
features_bot_false = vec.transform(str_list)
print(features_bot_false)



#DynamoDB
MY_ACCESS_KEY_ID = 'AKIAR3CZLWEYF7GITSGS'
MY_SECRET_ACCESS_KEY = '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'

resource = boto3.resource('dynamodb', aws_access_key_id=MY_ACCESS_KEY_ID, aws_secret_access_key=MY_SECRET_ACCESS_KEY, region_name='us-east-1')

df2 = df

for i in df2.columns:
    df2[i] = df2[i].astype(str)

myl=df2.T.to_dict().values()
#print(myl)
table = resource.Table('wikibot-title_cleaned')

for w in myl:
    print(w)
    table.put_item(Item=w)