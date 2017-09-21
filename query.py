import newspaper as nws
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import asyncio as sync
from sklearn.feature_extraction.text import TfidfVectorizer



################# for word vectorisation ##################
import re, math
from collections import Counter
import ast



##guardian_url = "https://www.theguardian.com/us-news/2017/feb/07/donald-trump-and-china-military-confrontation-dangerous-collision-course-experts"
guardian_url="https://www.theguardian.com/world/2017/apr/18/us-military-shoot-down-north-korea-missile-tests"
Location = r"/Users/darrelladjei/python/NewsApp/articleDB2.txt"
df = pd.read_csv(Location)
corpus= []
test_article = nws.Article(url=guardian_url, language='en')
test_article_kw = []
WORD = re.compile(r'\w+')
similarity_list=[]




##downloaded = False
##cnt=0




    

def build_it():

    downloaded = False

    cnt=0
    while not downloaded and cnt<2:
        
        test_article.download()

        try:

            test_article.parse()
            test_article.nlp()
            downloaded = True

        except:
            
            print("\nthere was an issue\n")
            downloaded = False
            cnt+=1


    if downloaded:
        global test_article_kw
        test_article_kw = test_article.keywords
        test_article_kw = ' '.join(test_article_kw)
##        print (test_article_kw)
  
    else:
        print('nothing to declare')




def transform_kw():

    for i in range(len(df.index)):
        
        kw_string_list= df.loc[i]['key_words']
        kw_list = ast.literal_eval(kw_string_list)
        kw = ' '.join(kw_list)
        corpus.append(kw)

##    print(corpus)
         

        

def get_similarity():


    df_size = len(df.index)

    global similarity_list
    
    similarity_list = np.zeros(df_size)

##    print(type(corpus[0]))
  

    for i in range(df_size):

        vec1 = text_to_vector(corpus[i])
        vec2 = text_to_vector(test_article_kw)
##        print('vec2',vec2)
##        print(test_article_kw)
    
        similarity = get_cosine(vec1,vec2)
##        print('sim',similarity)
        similarity_list[i] = similarity

##    print('the similarity list',similarity_list)



def get_most_similar():

##    print('similarity',similarity_list)
    max_match = max(similarity_list)
##    print('this is the max',max_match)

    all_best_matches = [i for i, j in enumerate(similarity_list) if abs(j)>=0.2]

##    print(similarity_list)
    for i in all_best_matches:
 
        print(df.loc[i]['Title']+'\n'+'\n'+test_article.title)
       

        
     




def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator



def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

    


def run():


    build_it()
    transform_kw()
    get_similarity()
    get_most_similar()
    


run()















