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

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data)

@app.route('/author')
def author_ui():
    return render_template('author.html')

@app.route('/recommend_by_author', methods=['POST'])
def recommend_by_author():
    user_input = request.form.get('user_input')
    data = []
    found_books = False

    if user_input in author_to_books:
        author_books = author_to_books[user_input]
        processed_books = set()
        
        for book in author_books:
            if book in pt.index and book not in processed_books:
                index = np.where(pt.index == book)[0][0]
                similar_items = sorted(list(enumerate(similarity_scores[index])), 
                                 key=lambda x: x[1], reverse=True)[1:5]
                
                for i in similar_items:
                    item = []
                    temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                    data.append(item)
                    found_books = True
                processed_books.add(book)

    if not found_books:
        return render_template('author.html', data=None, message=f"No recommendations found for '{user_input}'")
    
    return render_template('author.html', data=data, message=None)
