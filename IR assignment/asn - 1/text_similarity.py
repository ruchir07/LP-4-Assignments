from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Two input documents
doc1 = "Data science uses Python for analysis"
doc2 = "Python is useful for data analysis"

# Convert documents into numerical vectors
vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform([doc1, doc2])

# Calculate cosine similarity
similarity = cosine_similarity(vectors[0], vectors[1])

print("Document 1:", doc1)
print("Document 2:", doc2)
print("Similarity Score:", round(similarity[0][0], 4))
print("Similarity Percentage:",
      round(similarity[0][0] * 100, 2), "%")