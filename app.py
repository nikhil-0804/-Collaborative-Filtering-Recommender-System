from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import requests
from collections import defaultdict

# Load precomputed data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Create mappings
author_to_books = books.groupby('Book-Author')['Book-Title'].apply(list).to_dict()
book_to_author = defaultdict(list)
for author, titles in author_to_books.items():
    for title in titles:
        book_to_author[title].append(author)

app = Flask(__name__)
GOOGLE_BOOKS_API_KEY = ''

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
