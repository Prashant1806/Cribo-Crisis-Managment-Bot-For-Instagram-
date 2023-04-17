import os
import json
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Set up the NLTK sentiment analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Set up the stopword list for topic modeling
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Set up the TF-IDF vectorizer for topic modeling
tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)

# Set up the LDA model for topic modeling
lda_model = LatentDirichletAllocation(n_components=10,
                                      max_iter=10,
                                      learning_method='online',
                                      random_state=0)

def get_instagram_data(profile_url):
    # Get the Instagram API access token from the environment variable
    access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
    
    # Get the user ID for the given profile URL
    user_id_url = f'https://api.instagram.com/v1/users/self/?access_token={access_token}'
    user_id_response = requests.get(user_id_url)
    user_id_json = json.loads(user_id_response.text)
    user_id = user_id_json['data']['id']
    
    # Get the recent media for the user ID
    media_url = f'https://api.instagram.com/v1/users/{user_id}/media/recent/?access_token={access_token}'
    media_response = requests.get(media_url)
    media_json = json.loads(media_response.text)
    
    # Get the comments and messages from the recent media
    comments = []
    messages = []
    for post in media_json['data']:
        post_id = post['id']
        
        # Get the comments for the post
        comments_url = f'https://api.instagram.com/v1/media/{post_id}/comments?access_token={access_token}'
        comments_response = requests.get(comments_url)
        comments_json = json.loads(comments_response.text)
        for comment in comments_json['data']:
            comments.append(comment['text'])
        
        # Get the messages for the post (if it's a direct message)
        if post['type'] == 'raven_media':
            messages_url = f'https://api.instagram.com/v1/direct/{post_id}/thread/?access_token={access_token}'
            messages_response = requests.get(messages_url)
            messages_json = json.loads(messages_response.text)
            for message in messages_json['thread']:
                if message['item_type'] == 'text':
                    messages.append(message['text'])
    
    return comments, messages

def analyze_sentiment(text):
    # Use the NLTK sentiment analyzer to get the sentiment score for the text
    sentiment_scores = sia.polarity_scores(text)
    return sentiment_scores['compound']

def analyze_topics(texts):
    # Use the TF-IDF vectorizer to convert the text to a matrix of word counts
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    
    # Use the LDA model to fit the matrix and get the topics
    lda_model.fit(tfidf_matrix)
    topics = []
    for topic in lda_model.components_:
        topic_words = [tfidf_vectorizer.get_feature_names()[i] for i in topic.argsort()[:-11:-1]]
        topics.append(topic_words)
    
    return topics
