import newspaper as nws
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import asyncio as sync

async def wait_for(action,article):
    if action.lower() == 'download':
        await article.download()
        
    elif action.lower() == 'parse':
        await article.parse()

    elif action.lower() == 'nlp':
        await article.nlp()
        
cnn_paper = nws.build('http://edition.cnn.com/', memoize_articles=False)

print(cnn_paper.size())

##creating dataset
df = pd.DataFrame(columns=['Date','Title', 'key_words'])

missed = 0

for i in range(cnn_paper.size()):
    article = cnn_paper.articles[i]
    downloaded = False
    cnt=0
    while not downloaded and cnt<2:
        article.download()
        try:
            article.parse()
            article.nlp()
            downloaded = True
        except:
            print("\nthere was an issue\n")
            downloaded = False
            cnt+=1
    if downloaded:
        article_date = article.publish_date
        article_kw = article.keywords
        try:
            article_date.isoformat()
        except:
            pass
        df.loc[i] = [article_date,article.title,article_kw]
    else:
        missed+=1

path = "/Users/darrelladjei/python/NewsApp/articleDB2.txt"

df.to_csv(path,index=True,header=True)
