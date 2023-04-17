import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))

lemmatizer = WordNetLemmatizer()

def clean_text(text):
    # Remove URLs and mentions from the text
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@[^\s]+', '', text)
    # Remove all non-alphanumeric characters and convert to lowercase
    text = re.sub(r'\W+', ' ', text.lower())
    # Remove all whitespace characters
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def tokenize(text):
    # Use NLTK's word_tokenize function to tokenize the text
    tokens = word_tokenize(text)
    return tokens

def remove_stopwords(tokens):
    # Remove stop words from the token list
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens

def lemmatize(tokens):
    # Lemmatize the tokens using WordNetLemmatizer
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens
