from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from instagram_analysis import analyze_profile
from sentiment_analysis import get_sentiment
from topic_modeling import get_topics

app = Flask(__name__)

# Create a new ChatBot instance
bot = ChatBot('Influencer Crisis Management Bot')

# Train the chatbot on the ChatterBot corpus
trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.english')

# Define the Flask routes for the chatbot and the user interface
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get the message text from the POST request
    message = request.form['message']
    # Analyze the profile to get the number of followers and posts
    profile_url = request.form['profile_url']
    num_followers, num_posts = analyze_profile(profile_url)
    # Perform sentiment analysis on the message
    sentiment = get_sentiment(message)
    # Perform topic modeling on the message
    topics = get_topics([message], num_topics=3)
    # Generate a response from the chatbot
    response = bot.get_response(message)
    # Return the response as a JSON object
    return jsonify({
        'response': str(response),
        'num_followers': num_followers,
        'num_posts': num_posts,
        'sentiment': sentiment,
        'topics': topics
    })

if __name__ == '__main__':
    app.run(debug=True)
