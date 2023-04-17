from textblob import TextBlob
from nlp_utils import clean_text, tokenize, remove_stopwords

def get_sentiment(text):
    # Clean and preprocess the text
    clean_text = clean_text(text)
    tokens = tokenize(clean_text)
    tokens = remove_stopwords(tokens)
    # Join the list of tokens back into a string
    clean_text = ' '.join(tokens)
    # Use TextBlob to get the sentiment polarity
    blob = TextBlob(clean_text)
    sentiment_polarity = blob.sentiment.polarity
    return sentiment_polarity
