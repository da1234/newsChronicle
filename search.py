from theguardian import theguardian_content
import newspaper as nws
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import asyncio as sync
from sklearn.feature_extraction.text import TfidfVectorizer
from google.cloud import language



################# for word vectorisation ##################
import re, math
from collections import Counter
import ast



##test_url = "https://www.theguardian.com/us-news/2017/feb/07/donald-trump-and-china-military-confrontation-dangerous-collision-course-experts"
##test_url="https://www.theguardian.com/world/2017/apr/18/us-military-shoot-down-north-korea-missile-tests"
##df = pd.read_csv(Location)
##corpus= []
##test_article = nws.Article(url=guardian_url, language='en')
##test_article_kw = []
##WORD = re.compile(r'\w+')
##similarity_list=[]




class MainApp:


    def __init__(self,test_url):

        self.test_url = test_url
        self.language_client = language.Client()

        self.paper_dic = {

            'guardian':{

                "api_key":"54c650a2-8ab0-4a35-9417-7f2111fd29e7",
                "url_headers":{}},
            'cnn':{},
            'NYT':{},

            }

        self.set_url_headers()
        self.get_timeline()



    def set_url_headers(self,paper='guardian'):

        article_kw = self.get_test_article_kw().split()


        q = ''

##        for kw in article_kw:
##
##            if kw in self.article_summary:
##                extra ='AND'+' '+kw+' '
##                q+= extra
##
##            else:
##                pass

        
        print ('\nthese are the self entities: {}'.format(self.entity_list))
        for kw in self.entity_list :

            kw = kw.replace(" ", "-")

            extra ='AND'+' '+kw+' '
            q+= extra

                        
        q = q[3:]

        print("these are the query keywords: {}".format(q))
        
        headers = {
                    "q": q,
                    "order-by": "newest",
                    "from-date": "2012-01-01",
                    
            }



        if paper == 'guardian':

            self.paper_dic['guardian']['url_headers'] = headers

        





    def get_test_article_kw(self):

        self.entity_list = []
        self.entity_dic = {}
        
        test_article = nws.Article(url=self.test_url, language='en')
            
        downloaded = False

        cnt=0
        while not downloaded and cnt<2:
            
            test_article.download()

            try:

                test_article.parse()
                test_article.nlp()
                downloaded = True

            except:
                
##                print("\nthere was an issue\n")
                downloaded = False
                cnt+=1


        if downloaded:
    
            test_article_kw = test_article.keywords
            self.test_article_kw = ' '.join(test_article_kw)
            self.article_summary = test_article.summary
            test_article_text = test_article.text
            test_article_title = test_article.title



            ##### analysing the main txt itself

            document = self.language_client.document_from_text(test_article_text) ## changed form article title 
            entities = document.analyze_entities().entities          # Detects the entities of the text

            for ent in entities:

                if ent.metadata or ent.entity_type != 'OTHER':  

                    self.entity_dic[ent.name] = ent.salience

                    
   
            ### sorting dictionary ##

            n_keywords = sorted(self.entity_dic.items(),
                          key=lambda x: (x[1], x[0]),
                          reverse=True)

            
            self.entity_list = [j[0] for i,j in enumerate(n_keywords)][:5]
            self.salience_list = [j[1] for i,j in enumerate(n_keywords)][:5]

            print ('\nthis is the test title: {}'.format(test_article_title))


            print ('\nthese are the title entities and their salience: {entity}, {salience}'.format(entity=self.entity_list,salience=self.salience_list))
                 
            print ('\nthis is the summary: {}'.format(self.article_summary))
            
            return self.test_article_kw
      
        else:
            print('nothing to declare')


        

        

    def get_paper_articles(self,name ='guardian'):

        articles = []

        if name =='guardian':

            print('getting paper articles')

            article_urls = self._get_guardian_article_urls()
            articles = self._make_article_objs(article_urls)

        return articles
            

            

       
  

    def _get_guardian_article_urls(self):



        response_articles = []

        headers = self.paper_dic['guardian']['url_headers']

        # create content
        content = theguardian_content.Content(api= self.paper_dic['guardian']['api_key'], **headers)

        response_headers = content.response_headers()

        print("request response: {}".format(response_headers) )

        no_pages = response_headers['pages']
        self.no_results = response_headers['total']

        print("total results: {}".format(self.no_results ))
        
    
        ### get all results from all pages
        for page in range(1,no_pages+1):

##            print("Current page:{}".format(content.response_headers()['currentPage']))

            json_content = content.get_content_response(headers={"page":page})
            all_results = content.get_results(json_content)

            for res in all_results:
                
                db_entity_dic ={}
                response_articles.append(res['webUrl'])
##                print(" result title {}.".format(res['webTitle']))


        return response_articles













    def _make_article_objs(self,articles):

        for i,j in enumerate(articles):

            articles[i] = nws.Article(url=j, language='en')

        return articles

            





    def get_timeline(self):

        df = pd.DataFrame(columns=['Date','Title', 'key_words'])
        articles = self.get_paper_articles()
##        group_sz = 4
        group_sz = int(self.no_results /10.)
        group=[]
        missed = 0

        articles_sz = len(articles)


        remainder = len(articles)%group_sz

        for i in range(articles_sz):

            if articles_sz-i ==remainder:
                
                group_sz = articles_sz-i

            article = articles[i]
            ent_dic = {}

            downloaded = False
            cnt=0
    



            while not downloaded and cnt<2:
                
                article.download()

                try:

                    article.parse()
                    article.nlp()
                    downloaded = True

                except:
                    
##                    print("\nthere was an issue\n")
                    downloaded = False
                    cnt+=1


            if downloaded:
 
                article_text = article.text
                article_title = article.title
                article_date = article.publish_date
                article_summary = article.summary

                group.append(article_text) ## changed from article summary 

    
        

            else:

                missed+=1
                

            if len(group)==group_sz:

                matrix = self.get_sim_matrix(*group)
                collapsed_matrix = matrix.sum(axis=0)  ###sum the columns to guestimate highest cluster coeff
                print('THIS IS COLLAPSED MATRIX: {}'.format(collapsed_matrix))
                max_arg = np.argmax(collapsed_matrix)
                print('THIS IS MAX ARG: {}'.format(max_arg))
                            

                document = self.language_client.document_from_text(group[max_arg]) 
                entities = document.analyze_entities().entities          # Detects the entities of the text

                for ent in entities:

                   if ent.metadata or ent.entity_type != 'OTHER':

                        ent_dic[ent.name] = ent.salience
    



                n_keywords = sorted(ent_dic.items(),
                              key=lambda x: (x[1], x[0]),
                              reverse=True)

                 
                entity_list = [j[0] for i,j in enumerate(n_keywords)][:5]
                salience_list = [j[1] for i,j in enumerate(n_keywords)][:5]


                print('\nfor article titled: {}'.format(article_title))
                print('published on: {}'.format(article_date.isoformat()))
                print('these are the key_words: {}'.format(entity_list))

                group=[]

                









    def get_sim_matrix(self,*summaries):


        vect = TfidfVectorizer(min_df=1)

        tfidf = vect.fit_transform([*summaries])

        print("similarity matrix: {}".format((tfidf * tfidf.T).A))

        return (tfidf * tfidf.T).A




##app = MainApp(test_url = "http://edition.cnn.com/2017/04/25/politics/trump-north-korea-taunts/index.html")

##https://www.theguardian.com/politics/2017/apr/27/theresa-may-to-lay-bare-ambition-to-capture-labour-heartlands
##"https://www.theguardian.com/politics/2017/apr/25/leaked-labour-script-puts-core-party-issues-above-brexit"
##"http://edition.cnn.com/2017/04/26/politics/donald-trump-100-days-poll/index.html"
##"http://edition.cnn.com/2017/04/28/europe/french-election-russia/index.html"
##https://www.theguardian.com/environment/2017/jun/03/michael-bloomberg-us-states-and-businesses-will-still-meet-paris-targets
app = MainApp(test_url ="https://www.theguardian.com/environment/2017/jun/03/michael-bloomberg-us-states-and-businesses-will-still-meet-paris-targets")        
    
        

        

        

    


    



























































##
##
##
##
##
##
##
##api_key = "54c650a2-8ab0-4a35-9417-7f2111fd29e7"
##
##
##headers = {
##            "q":'Trump AND north-korea',
##            "order-by": "newest",
##            "from-date": "2012-01-01",
##            "section": "world",
##    }



