import numpy as np
import pickle

similarity = pickle.load(open("similarity.pkl", "rb"))

top_k = 50
top_similar_movies = []

for i in range(len(similarity)):
    similar_indices = np.argsort(similarity[i])[-top_k-1:-1]
    top_similar_movies.append(similar_indices)

pickle.dump(top_similar_movies, open("similarity.pkl", "wb"))