from sklearn.feature_extraction.text import TfidfVectorizer

import newspaper as nws

import numpy as np





guardian_url_1="https://www.theguardian.com/environment/2017/jun/03/michael-bloomberg-us-states-and-businesses-will-still-meet-paris-targets"
guardian_url_2 = "https://www.theguardian.com/us-news/2017/jun/01/pittsburgh-fires-back-trump-paris-agreement"
guardian_url_3 = "https://www.theguardian.com/environment/2017/jun/02/european-leaders-vow-to-keep-fighting-global-warming-despite-us-withdrawal"




guardian_urls = [guardian_url_1,guardian_url_2,guardian_url_3]
corpus= []




def build():


    for guardian_url in guardian_urls:

        test_article = nws.Article(url=guardian_url, language='en')

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
            test_article_summary = test_article.summary

            print("\nthis was the summary: {}".format(test_article_summary))
            corpus.append(test_article_summary)
      
        else:
            print('did not parse well')





def get_sim_matrix():


        vect = TfidfVectorizer(min_df=1)



        tfidf = vect.fit_transform(['it is a cold day',
                                'the temperature low'])


        print("similarity matrix: {}".format((tfidf * tfidf.T).A))


##build()

get_sim_matrix()







            
