import streamlit as st
import praw
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go


reddit = praw.Reddit(client_id=st.secrets["client_id"], client_secret=st.secrets["client_secret"], user_agent="sentiment")

#List of text
wordsc=[]
substop= reddit.subreddit('wallstreetbets').hot(limit=250)
for sub in substop:
    text=sub.selftext
    text_wds=text.split()
    wordsc.append(text_wds)

wordsct=[]
substop= reddit.subreddit('wallstreetbets').hot(limit=250)
for sub in substop:
    title=sub.title
    title_wds=title.split()
    wordsct.append(title_wds)
    
wordsc=wordsct+wordsc

#Build a list of words from the array.
newwordsc = []
for i in wordsc:
    for j in i:
        newwordsc.append(j)

#Extract tickers
stock_symbol=[]
for word in newwordsc:
    if word[0]=='$':
        stock_symbol.append(word)
        
cloud1=[]
for i in newwordsc:
    i=''.join(filter(str.isalpha, i))
    cloud1.append(i)

while("" in cloud1) :
    cloud1.remove("")
    
#Build the word cloud.
st.set_option('deprecation.showPyplotGlobalUse', False)
wordcloud = WordCloud(width = 1000, height = 500).generate(" ".join(cloud1))
fig=plt.figure(figsize=(15,8))
fig=plt.imshow(wordcloud)
fig=plt.axis("off")
fig=plt.show()
st.pyplot(fig)
plt.close()       
