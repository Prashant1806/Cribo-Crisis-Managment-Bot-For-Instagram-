import gensim
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
from nlp_utils import clean_text, tokenize, remove_stopwords, lemmatize

def get_topics(texts, num_topics):
    # Clean and preprocess the text
    preprocessed_texts = [lemmatize(remove_stopwords(tokenize(clean_text(text)))) for text in texts]
    # Create a dictionary and corpus
    dictionary = Dictionary(preprocessed_texts)
    corpus = [dictionary.doc2bow(text) for text in preprocessed_texts]
    # Train an LDA model
    lda_model = LdaModel(corpus=corpus,
                         id2word=dictionary,
                         num_topics=num_topics,
                         random_state=42,
                         passes=10)
    # Get the topic distribution for each text
    topic_distributions = [lda_model.get_document_topics(corpus[i]) for i in range(len(corpus))]
    # Extract the top topic for each text
    top_topics = [max(topics, key=lambda x: x[1])[0] for topics in topic_distributions]
    return top_topics
