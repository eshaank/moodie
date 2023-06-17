# My OpenAI Key
import os
os.environ['OPENAI_API_KEY'] = ""

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import VectorStoreIndex, SimpleDirectoryReader


documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("I've been feeling depressed. What movie can I watch to feel better?")
print(response)

#def sort_movies():
