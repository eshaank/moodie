from flask import Flask, render_template, request
import os

os.environ['OPENAI_API_KEY'] = "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"

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import VectorStoreIndex, SimpleDirectoryReader

app = Flask(__name__)

# Load your index and set up the query engine
documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()\

#move ratings and feedback
movies = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def recommend():
    query = request.form['query']
    response = query_engine.query(query)
    return render_template('home.html', query=query, response=response)

@app.route('/rate', methods=['GET', 'POST'])
def rate():
    if request.method == 'POST':
        movie = request.form['movie']
        rating = int(request.form['rating'])
        feedback = request.form['feedback']
        movies[movie] = (rating, feedback)
        return render_template('rate.html', movies=movies)
    else:
        return render_template('rate.html', movies=movies)
    

# def index_documents(movie_feedbacks):
#     # Index the documents (movies) with their corresponding feedbacks as their content
#     documents = []
#     for movie, feedback in movie_feedbacks.items():
#         documents.append((movie, feedback))
#     index.add_documents(documents)
#     index.persist()

# def get_recommendations(query):
#     query_results = query_engine.query(query)
#     similar_movies = [result['document'] for result in query_results]

#     # Content-Based Filtering: Find movies similar to previously watched ones
#     watched_movies = [movie for movie in movies.keys()]
#     similar_to_watched = get_similar_movies(watched_movies)

#     # Collaborative Filtering: Find movies with similar user feedback/feelings
#     similar_feelings = get_similar_feelings(query)

#     # Combine recommendations from both approaches
#     recommendations = set(similar_movies + similar_to_watched + similar_feelings)

#     # Exclude movies the user has already watched
#     recommendations = [movie for movie in recommendations if movie not in watched_movies]

#     return recommendations[:5]  # Return top 5 recommendations

if __name__ == '__main__':
    app.run()
