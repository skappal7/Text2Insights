# Text2Insights

Welcome to Text2Insights! This application allows you to upload a CSV file containing customer reviews and perform various text and sentiment analysis tasks. The app is built using Streamlit and provides an interactive and visually appealing interface for your text analysis needs.

## Features

- **Word Cloud**: Generate a word cloud to visualize the most frequent words in your text data.
- **Text Analytics**: View a table of word frequencies for deeper insights into your text data.
- **Sentiment Analysis**: Analyze the sentiment of your text data and visualize the distribution of positive, negative, and neutral sentiments.
- **N-grams**: Explore the most common bigrams and trigrams in your text data.
- **Top Words**: Identify the top 20 positive and negative words in your text data.
- **Download Results**: Download the analysis results as a CSV file.

## Demo

Check out the live demo of the app on Streamlit Share: [Text2Insights](https://share.streamlit.io/skappal7/text2insights/main)

## Installation

To run the app locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/skappal7/text2insights.git
    cd text2insights
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app**:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Upload a CSV file containing a column named `Review` with your text data.
2. Optionally, specify words to exclude from the analysis, set the minimum word frequency, and the maximum number of words to display in the word cloud.
3. Navigate through the tabs to view the word cloud, text analytics, sentiment analysis, n-grams, and top words.
4. Download the analysis results as a CSV file using the download button.

## Example CSV Format

Your CSV file should look like this:

```csv
Review
"I love this product! It's amazing."
"This is the worst experience I've ever had."
"Great quality and fast shipping."
