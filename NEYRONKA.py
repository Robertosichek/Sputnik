# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Auxf46bor8ZSXR7yeBBr_Il6KBY515bj
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import pymorphy2

df = pd.read_csv("data.csv")



import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

import pymorphy2

nltk.download('stopwords')
nltk.download('punkt')

stop_words = stopwords.words("russian")

morph = pymorphy2.MorphAnalyzer()

def data_preprocessing(review):

  # tokenization
  tokens = word_tokenize(review)

  # stop words removal
  review = [morph.parse(word)[0].normal_form for word in tokens if word not in stop_words]

  review = ' '.join(review)

  return review

df['обработанные_жалобы'] = df['жалобы'].apply(lambda review: data_preprocessing(review))

df = df.drop(["жалобы"], axis = 1)

from sklearn.model_selection import train_test_split

data = df.copy()
y = data['специальность_врача'].values
data.drop(['специальность_врача'], axis=1, inplace=True)

X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=0.3)

print(f"Train data: {X_train.shape, y_train.shape}")
print(f"Test data: {X_test.shape, y_test.shape}")

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(min_df=10)

X_train_review_tfidf = vectorizer.fit_transform(X_train['обработанные_жалобы'])
X_test_review_tfidf = vectorizer.transform(X_test['обработанные_жалобы'])

print('X_train_review_tfidf shape: ', X_train_review_tfidf.shape)
print('X_test_review_tfidf shape: ', X_test_review_tfidf.shape)

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
clf = MultinomialNB(alpha=1)
clf.fit(X_train_review_tfidf, y_train)

y_pred = clf.predict(X_test_review_tfidf)
print('Test Accuracy: ', accuracy_score(y_test, y_pred))

from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(penalty='l2')
clf.fit(X_train_review_tfidf, y_train)

y_pred = clf.predict(X_test_review_tfidf)
print('Test Accuracy: ', accuracy_score(y_test, y_pred))

a = input()
a = a.lower()
a = a.replace(',', '')
a = a.replace('-', '')
a = a.replace('.', '')

preprocessed_input = data_preprocessing(a)
test = np.array([preprocessed_input])
test_series = pd.Series(test)
test_tfidf = vectorizer.transform(test_series)

pred = clf.predict(test_tfidf)
pred

