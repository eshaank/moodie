from flask import Flask, render_template, request
#from dotenv import load_dotenv
import os

#load_dotenv()

os.environ['OPENAI_API_KEY'] = ""


import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import (VectorStoreIndex, SimpleDirectoryReader, QuestionAnswerPrompt, LLMPredictor, GPTVectorStoreIndex)
from langchain import OpenAI

app = Flask(__name__)

# Load your index and set up the query engine
documents = SimpleDirectoryReader('data').load_data()

index = VectorStoreIndex.from_documents(documents)
#index = GPTVectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

#move ratings and feedback
movies = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def recommend():
    query_before = request.form['query_before']
    query_after = request.form['query_after']

    indexed_movies = index_documents(movies, query_before, query_after)


    QA_PROMPT_TMPL = (
        "We have provided context information below.\n"
        "---------------------\n"
        f"I am feeling {query_before}. I want to feel {query_after} by the end of the movie. Can you recommend me some movies that are also similar to {indexed_movies}\n"
        "---------------------\n"
        "Please respond with a list of 3 movies in bullet point form and a line after each movie:\n"
    )


    print(QA_PROMPT_TMPL)

    mood_text = f"You are feeling {query_before}, so here are some movies to help you feel {query_after}"

    response = query_engine.query(QA_PROMPT_TMPL)
    #return render_template('recommendation.html')
    return render_template('home.html', query=mood_text, response=response)


@app.route('/rate', methods=['GET', 'POST'])
def rate():
    if request.method == 'POST':
        movie = request.form['movie']
        feedback = request.form['feedback']
        movies[movie] = (feedback)
        return render_template('rate.html', movies=movies)
    else:
        return render_template('rate.html', movies=movies)
    

def index_documents(movie_feedbacks, mood_before, mood_after):
    file_path = "./user_movies/user_preferences.txt"
    # Index the documents (movies) with their corresponding feedbacks as their content
    dict_documents = []
    for movie, feedback in movie_feedbacks.items():
        dict_documents.append((movie, feedback))
    

    with open(file_path, 'w') as file:
        for item in dict_documents:
            file.write(str(item) + '\n')


    docu = SimpleDirectoryReader('user_movies').load_data()
    dict_indexes = VectorStoreIndex.from_documents(docu)
    dict_query_eng = dict_indexes.as_query_engine()

   

    context = f"of the movies entered, which 3 most resemble the user's mood before: {mood_before} and after: {mood_after}"

    dict_response = dict_query_eng.query(context)
    print("THE USER'S MOVIES HISTORY: ", dict_response)
    return dict_response

# def recommend_movies(user_feedback):
#     # Index the user's feedback
#     index_documents(user_feedback)

#     # Perform a query to retrieve similar movies
#     query = " ".join(user_feedback.values())  # Use the aggregated feedback as the query
#     query_results = query_engine.query(query)

#     # Extract recommended movies from the query results
#     recommended_movies = [result['document'] for result in query_results]

#     return recommended_movies[:5]  # Return top 5 recommended movies


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
