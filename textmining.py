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
    data['sentiment_type'] =
