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