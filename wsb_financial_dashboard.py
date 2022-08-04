import streamlit as st
import praw
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go

st.title("Hot topics on r/wallstreetbets and trending securities")
reddit = praw.Reddit(client_id=st.secrets["client_id"], client_secret=st.secrets["client_secret"], user_agent="sentiment")

#List of text
wordsc=[]
substop= reddit.subreddit('wallstreetbets').hot(limit=150)
for sub in substop:
    text=sub.selftext
    text_wds=text.split()
    wordsc.append(text_wds)

wordsct=[]
substop= reddit.subreddit('wallstreetbets').hot(limit=150)
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

#Remove prices ex: $16.
stocksymbol = [x for x in stock_symbol if not any(x1.isdigit() for x1 in x)]

#Select uppercase words.
stockfinal=[]
for symbol in stocksymbol:
    if symbol.isupper():
        stockfinal.append(symbol)

#Remove cashtag and other non-alphabetic characters.
stocks=[]
for i in stockfinal:
    i=''.join(filter(str.isalpha, i))
    stocks.append(i)

#Remove false tickers   
trolls=['AMTD','CUM','CGX']
for troll in trolls:
    while troll in stocks: 
        stocks.remove(troll)
        
#Remove duplicates.
res = []
for i in stocks:
    if i not in res:
        res.append(i)
#trending securities      
df = pd.DataFrame (stocks, columns = ['Ticker'])
df=df.value_counts(['Ticker']).reset_index(name='Count')
figt = px.bar(df, x = "Ticker", y = "Count", title="Ticker frequency")
st.plotly_chart(figt)

#selectbox
st.subheader("Select a ticker :") 
ticker=st.selectbox('Pick a trending stock', res)
ticker= str(ticker)

data = yf.download(ticker, period='max',interval = '1d', rounding= True)

fig = go.Figure()
fig.add_trace(go.Candlestick())
fig.add_trace(go.Candlestick(x=data.index,open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))
fig.update_layout(title = 'Share price', yaxis_title = 'Stock Price (USD)')
                  
fig.update_xaxes(rangeslider_visible=True,rangeselector=dict(buttons=list([dict(step='all')])))

st.plotly_chart(fig)

#Display revenue and earnings

st.write("Earnings & Revenue")
fin = yf.Ticker(ticker)
df1 = pd.DataFrame(fin.quarterly_earnings)

fige = px.bar(df1, x=df1.index, y=df1.columns, barmode='group')

st.plotly_chart(fige)

st.stop()
