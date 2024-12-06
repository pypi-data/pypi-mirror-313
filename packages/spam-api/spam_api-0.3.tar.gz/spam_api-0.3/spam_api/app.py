import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

import joblib


texts = [
    "Congratulations! You've won a free ticket.",
    "Reminder: Your appointment is tomorrow.",
    "Claim your $1000 gift card now!",
    "Hello, how are you doing today?"
]
labels = [1, 0, 1, 0]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
model = MultinomialNB()
model.fit(X, labels)

joblib.dump((model, vectorizer), 'spam_detector_model.pkl')
print("Modelo guardado como 'spam_detector_model.pkl'")
