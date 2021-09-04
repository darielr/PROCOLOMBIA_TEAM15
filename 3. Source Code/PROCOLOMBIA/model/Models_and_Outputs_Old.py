
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
from wordcloud import WordCloud , STOPWORDS, ImageColorGenerator
from PIL import Image
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt
import string
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import pyLDAvis
import pyLDAvis.sklearn
from nltk.sentiment import SentimentIntensityAnalyzer
#nltk.download('wordnet') # Se corre una única vez....
#nltk.download('vader_lexicon') # Se corre una única vez....

#%%

# Clean Function 1

def tildes(text):
    
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ", "n")
    )
    
    for a, b in replacements:
        text = text.replace(a, b).replace(a.upper(), b.upper())  
    return text

# Clean Function 2

def strip_links(text):
    
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

# Clean Function 3

def strip_all_entities(text):
    
    entity_prefixes = ['@','#']
    
    for separator in  string.punctuation:
        if separator not in entity_prefixes:
            
            text = text.replace(separator,' ')
            
    words = []
    
    for Word in text.split():
        
        Word = Word.strip()
        
        if Word:
            
            if Word[0] not in entity_prefixes:
                words.append(Word)
                
    return ' '.join(words)

# Most frequently occuring Word

def get_top_n_words(corpus, n = None):
    
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis = 0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse = True)
    return words_freq[:n]

# Most frequently occuring Bi-grams

def get_top_n2_words(corpus, n = None): 
    vec1 = CountVectorizer(ngram_range = (2,2), max_features = 2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis = 0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec1.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse = True)
    return words_freq[:n]
    
# Most frequently occuring Tri-grams

def get_top_n3_words(corpus, n = None):
    vec1 = CountVectorizer(ngram_range = (3,3), max_features = 2000).fit(corpus) 
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis = 0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec1.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

# Clean Function Def

def cleanning(data):
    
    corpus = []
    
    for index, row in usa.iterrows():
      
        text = row['text']
  
      #Remove punctuations
      
        text = tildes(text)
        text = strip_links(text)
        text = strip_all_entities(text)  
  
      #Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ', text)
  
      #Convert to lowercase
        text = text.lower()  
          
      #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
      
      # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
      
      ##Convert to list from string
        text = text.split()
      
      #Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in stop_words] 
        text = " ".join(text)
      
        corpus.append(text)
        
    return corpus 

# Sentiment Analysis Function

def sentiment(corpus, country):
    
    path = '/home/ubuntu/PROCOLOMBIA/assets/'
        
    sia = SentimentIntensityAnalyzer()
    tweetdf=pd.DataFrame(corpus)
    tweetdf.columns=['tweet']
    tweetdf['score']=tweetdf.apply(lambda row : sia.polarity_scores(row['tweet']), axis = 1)
    tweetdf=pd.concat([tweetdf.drop(['score'],axis=1),tweetdf['score'].apply(pd.Series)],axis=1)
 
    def sentiment_result(compound):
        if compound>=0.05:
            return "Positive"
        elif compound<=-0.05:
            return "Negative"
        else :
            return "Neutral"
  
    tweetdf['sentiment']=tweetdf.apply(lambda row: sentiment_result(row['compound']),axis=1)
    figsentiment=px.histogram(tweetdf,x='compound',title="Score histogram")
    figsentiment.write_html(path + country + "_figsentiment.html")
    tablesent=tweetdf["sentiment"].value_counts()
    sentimentbar=px.bar(y=tablesent,x=tablesent.index,title="Sentiment Analysis")
    sentimentbar.write_html(path + country + "_sentimentbar.html")
   

# Topic Modeling function

def topic(corpus, country):
    
    path = '/home/ubuntu/PROCOLOMBIA/assets/'
    
    docs_raw = corpus
  
    tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                  stop_words = stop_words,
                                  lowercase = True,
                                  token_pattern = r'\b[a-zA-Z]{3,}\b',
                                  max_df = 0.5, 
                                  min_df = 10)
  
    dtm_tf = tf_vectorizer.fit_transform(docs_raw)
    tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
    dtm_tfidf = tfidf_vectorizer.fit_transform(docs_raw)
  
  
    lda_tf = LatentDirichletAllocation(n_components = 5, random_state = 0)
  
    lda_tf.fit(dtm_tf)
  
  
    lda_tfidf = LatentDirichletAllocation(n_components = 5, random_state = 0)
  
    lda_tfidf.fit(dtm_tfidf)
  
    html_file = pyLDAvis.sklearn.prepare(lda_tf, dtm_tf, tf_vectorizer)
  
    pyLDAvis.save_html(html_file, path + country + '_lda.html')

#%%

# Word Cloud Function

def wordcloud_func(corpus, country):
    
    path = '/home/ubuntu/PROCOLOMBIA/assets/'
    
    wordcloud = WordCloud( background_color = 'white', 
                          stopwords = stop_words, 
                          max_words = 100,
                          max_font_size = 50, 
                          random_state = 0).generate(str(corpus))
    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
    fig.savefig(path + country + "_wordcloud1.png", dpi = 900)

#%%

# Unigram, Bigrams, trigrams Function

def uni_big_trig(corpus, country):
    
    path = '/home/ubuntu/PROCOLOMBIA/assets/'
    
    # Most freq words dataframe
    top_words = get_top_n_words(corpus, n = 10)
    top_df = pd.DataFrame(top_words)
    top_df.columns=["Word", "Freq"]
    
    # Bigramas
    top2_words = get_top_n2_words(corpus, n = 10)
    top2_df = pd.DataFrame(top2_words)
    top2_df.columns=["Bi-gram", "Freq"]
    
    # Tri-grams
    top3_words = get_top_n3_words(corpus, n = 10)
    top3_df = pd.DataFrame(top3_words)
    top3_df.columns=["Tri-gram", "Freq"]
    
    barchartOnegram = px.bar(x = top_df['Word'], y = top_df['Freq'], title = 'BarOnegram')
    barchartBigram = px.bar(x = top2_df['Bi-gram'], y = top2_df['Freq'], title = 'BarBigram')
    barchartTrigram = px.bar(x = top3_df['Tri-gram'], y = top3_df['Freq'], title = 'BarTrigram')
    
    barchartOnegram.write_html(path + country + "_barchartOnegram.html")
    barchartBigram.write_html(path + country + "_barchartBigram.html")
    barchartTrigram.write_html(path + country + "_barchartTrigram.html")

#%%

# All Outputs

def all_outputs(df_def, country):

    corpus = cleanning(df_def['text'])
    
    wordcloud_func(corpus, country)
    
    uni_big_trig(corpus, country)

    sentiment(corpus, country)

    topic(corpus, country)
    
#%%

# Creating a list of stop words and adding custom stopwords

stop_words = set(stopwords.words('english','spanish'))

# Creating a list of custom stopwords

new_words = ['http', 'rt']
stop_words = stop_words.union(new_words)

#%%

# Creating dataframes

path = '/home/ubuntu/PROCOLOMBIA/data/'

usa = pd.read_csv(path + 'USA_df_tw.csv', encoding = 'latin1')
uk = pd.read_csv(path + 'UK_df_tw.csv', encoding = 'latin1')
canada = pd.read_csv(path + 'Canada_df_tw.csv', encoding = 'latin1')

#%%

# Run All

all_outputs(usa, 'USA')
all_outputs(uk, 'UK')
all_outputs(canada, 'Canada')






