import nltk
nltk.download('stopwords')

import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.util import ngrams
import altair as alt
from collections import Counter
from textblob import TextBlob

# Set page configuration
st.set_page_config(page_title="Text and Sentiment Preliminary Analysis", layout="wide")

# Custom CSS for a modern design
st.markdown("""
    <style>
        .css-1d391kg {
            background-color: #333333 !important;
            color: #FAFAFA !important;
        }
        .css-145kmo2 {
            background-color: #07B1FC !important;
            color: #FAFAFA !important;
        }
        .css-18e3th9 {
            color: #333333 !important;
        }
        .stButton>button {
            background-color: #07B1FC !important;
            color: white !important;
            border: none !important;
            border-radius: 5px !important;
        }
        .stNumberInput>div>input {
            background-color: #FAFAFA !important;
            color: #333333 !important;
        }
        .stTextInput>div>input {
            background-color: #FAFAFA !important;
            color: #333333 !important;
        }
        .css-1aumxhk {
            color: #FAAF3B !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load stopwords
stop_words = set(stopwords.words('english'))

# Sidebar for file upload and input parameters
st.sidebar.header("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
exclude_words = st.sidebar.text_input("Words to Exclude (comma separated)", "")
min_freq = st.sidebar.number_input("Minimum Frequency", value=2, min_value=1)
max_words = st.sidebar.number_input("Maximum Words", value=200, min_value=1)

# Function to clean text
def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = ''.join([c for c in text if c not in ('!', '.', ':', ',', '?')])
        return text
    else:
        return ""

# Function to analyze text data
def analyze_text(data, column):
    data[column] = data[column].apply(clean_text)
    words = ' '.join(data[column]).split()
    words = [word for word in words if word not in stop_words]
    if exclude_words:
        exclude = exclude_words.split(',')
        words = [word for word in words if word not in exclude]
    return words

# Function to perform sentiment analysis
def sentiment_analysis(data, column):
    data['sentiment'] = data[column].apply(lambda x: TextBlob(x).sentiment.polarity if x else 0)
    data['sentiment_type'] = data['sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
    return data

# Plot word cloud
def plot_wordcloud(words):
    wordcloud = WordCloud(width=800, height=400, max_words=max_words, background_color='white').generate(' '.join(words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Plot sentiment analysis
def plot_sentiment(data):
    sentiment_counts = data['sentiment_type'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']
    chart = alt.Chart(sentiment_counts).mark_bar().encode(
        x='sentiment',
        y='count',
        color='sentiment'
    ).properties(
        title="Sentiment Analysis"
    )
    st.altair_chart(chart, use_container_width=True)

# Plot n-grams
def plot_ngrams(words, n):
    n_grams = ngrams(words, n)
    n_grams_freq = FreqDist(n_grams).most_common(50)
    n_grams_df = pd.DataFrame(n_grams_freq, columns=['ngram', 'count'])
    n_grams_df['ngram'] = n_grams_df['ngram'].apply(lambda x: ' '.join(x))
    chart = alt.Chart(n_grams_df).mark_bar().encode(
        x=alt.X('ngram', sort='-y'),
        y='count',
        tooltip=['ngram', 'count']
    ).properties(
        title=f"Top 50 {'Bigrams' if n == 2 else 'Trigrams'}"
    )
    st.altair_chart(chart, use_container_width=True)

# Plot top positive and negative words
def plot_top_words(data, sentiment):
    words = data[data['sentiment_type'] == sentiment]['Review'].str.cat(sep=' ').split()
    words = [word for word in words if word not in stop_words]
    words_freq = Counter(words).most_common(20)
    words_df = pd.DataFrame(words_freq, columns=['word', 'count'])
    chart = alt.Chart(words_df).mark_bar().encode(
        x=alt.X('word', sort='-y'),
        y='count',
        color=alt.value('green' if sentiment == 'Positive' else 'red')
    ).properties(
        title=f"Top 20 {sentiment} Words"
    )
    st.altair_chart(chart, use_container_width=True)

# Main panel for displaying analysis
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if 'Review' in data.columns:
        words = analyze_text(data, 'Review')
        sentiment_data = sentiment_analysis(data, 'Review')

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Word Cloud", "Text Analytics", "Sentiment Analysis", "N-grams", "Top Words"])

        with tab1:
            st.header("Word Cloud")
            plot_wordcloud(words)

        with tab2:
            st.header("Text Analytics")
            text_freq = pd.DataFrame(FreqDist(words).most_common(), columns=['word', 'count'])
            st.dataframe(text_freq)

        with tab3:
            st.header("Sentiment Analysis")
            plot_sentiment(sentiment_data)
            st.dataframe(sentiment_data[['Review', 'sentiment', 'sentiment_type']])

        with tab4:
            st.header("N-grams")
            plot_ngrams(words, 2)
            plot_ngrams(words, 3)

        with tab5:
            st.header("Top Words")
            plot_top_words(sentiment_data, 'Positive')
            plot_top_words(sentiment_data, 'Negative')

        # Download button
        csv = sentiment_data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results", data=csv, file_name="results.csv", mime="text/csv")
    else:
        st.error("The uploaded CSV file does not contain a 'Review' column.")
else:
    st.info("Please upload a CSV file to analyze.")
