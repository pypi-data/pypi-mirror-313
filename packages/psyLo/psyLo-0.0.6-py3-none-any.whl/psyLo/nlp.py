# Imports

import re
import nltk
import string
import pandas as pd

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

from nltk.stem import WordNetLemmatizer, PorterStemmer

import subprocess
import sys

# Function to install a package using pip
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Example usage
install('textblob')
install('lime')
install('emoji')
install('gensim')
install('spacy')

import spacy
import emoji
from textblob import TextBlob
from lime.lime_text import LimeTextExplainer

import gensim.models
from gensim.models import Word2Vec

from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer

# Text Preprocessing

def rmExcessWhitespaces(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def rmHTML(text):
    rmHTML_pattern = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    text = re.sub(rmHTML_pattern, '', text)
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmURL(text):
    rmURL_pattern = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''')
    text = re.sub(rmURL_pattern, '', text)
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmSpecialChar(text):
    rmSpecialChar_pattern = re.compile(r'[^a-zA-Z0-9\s]')
    text = re.sub(rmSpecialChar_pattern, '', text)
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmEmojis(text):
    text = emoji.replace_emoji(text, replace='')
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmPunctuation(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmNumbers(text):
    # using just r'\d' ensures that spaces between numbers are preserved
    rmNumbers_pattern = re.compile(r'\d')
    text = re.sub(rmNumbers_pattern, '', text)
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def tokenize(text, tokenizeType='word'):
    match tokenizeType:
        case 'word':
            tokenized_text = word_tokenize(text)#text.lower())
        case 'sentence':
            tokenized_text = sent_tokenize(text)#text.lower())
        case 'char':
            tokenizer = RegexpTokenizer(r'\w')
            tokenized_text = tokenizer.tokenize(text)
        case _:
            print('Incorrect tokenizeType')
    return tokenized_text

def rmStopWords(list_words, stop_words):
    list_words = [ word for word in list_words if word not in stop_words ]
    return list_words

def wordNetLemmatize(list_words):
    wnl = WordNetLemmatizer()
    list_words_lemmatized = []
    for word in list_words:
        lemmatized_word = wnl.lemmatize(word)
        list_words_lemmatized.append(lemmatized_word)
    return list_words_lemmatized

def porterStemmer(list_words):
    ps = PorterStemmer()
    list_words_stemmed = [ps.stem(word) for word in list_words]
    return list_words_stemmed

# Data PreProcessing

def sentimentLogReg(df, text, target):

    X_train, X_test, y_train, y_test = train_test_split(df[text], df[target], test_size = 0.2, random_state = 42)

    tfidf_vectorizer = TfidfVectorizer(max_features=1000)

    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    logreg_model = LogisticRegression(max_iter = 1000)
    logreg_model.fit(X_train_tfidf, y_train)

    y_pred = logreg_model.predict(X_test_tfidf)
    
    y_pred_test = logreg_model.predict(X_test_tfidf[4])
    print(y_pred_test)

    return X_train, X_test, y_train, y_test, logreg_model, y_pred

def sentimentRandomForest(df, text, target):

    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))

    X = vectorizer.fit_transform(df[text])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

    model_rf = RandomForestClassifier(random_state = 42)
    model_rf.fit(X_train, y_train)
    
    y_pred = model_rf.predict(X_test)

    print(model_rf.predict(X_test[4]))

    return X_train, X_test, y_train, y_test, model_rf, y_pred

# Help Functions

def help():
    print(f"""

List of Available Functions:

    Text Preprocessing:
        1.  rmExcessWhitespaces(text)
        2.  rmHTML(text)
        3.  rmURL(text)
        4.  rmSpecialChar(text)
        5.  rmEmojis(text)
        6.  rmPunctuation(text)
        7.  rmNumbers(text)
        8.  tokenize(text, tokenizeType = ('word', 'sentence' or 'char'))
        9.  rmStopWords(list_tokens)
        10. wordNetLemmatize(list_tokens)
        11. porterStemmer(list_tokens)
        12. example()
          
    Sentiment Analysis:
        13. sentimentLogReg(df, text, target)
        14. sentimentRandomForest(df, text, target)
          
        Both return:  X_train, X_test, y_train, y_test, model_rf, y_pred
    
    Print Source:
        1. sourceTextPreprocessing()
        2. sourceSentimentAnalysis()

    """)

def example():
    print("\nExample: dataframe['cleanText'] = data['text'].apply(rmURL)\n")

def sourceTextPreprocessing():
    print(
"""

# Text Preprocessing

def rmExcessWhitespaces(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def rmHTML(text):
    rmHTML_pattern = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    text = re.sub(rmHTML_pattern, '', text)
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmURL(text):
    rmURL_pattern = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''')
    text = re.sub(rmURL_pattern, '', text)
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmSpecialChar(text):
    rmSpecialChar_pattern = re.compile(r'[^a-zA-Z0-9\s]')
    text = re.sub(rmSpecialChar_pattern, '', text)
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmEmojis(text):
    text = emoji.replace_emoji(text, replace='')
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmPunctuation(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def rmNumbers(text):
    # using just r'\d' ensures that spaces between numbers are preserved
    rmNumbers_pattern = re.compile(r'\d')
    text = re.sub(rmNumbers_pattern, '', text)
    # removing excess white spaces
    text = rmExcessWhitespaces(text)
    return text

def tokenize(text, tokenizeType='word'):
    match tokenizeType:
        case 'word':
            tokenized_text = word_tokenize(text)#text.lower())
        case 'sentence':
            tokenized_text = sent_tokenize(text)#text.lower())
        case 'char':
            tokenizer = RegexpTokenizer(r'\w')
            tokenized_text = tokenizer.tokenize(text)
        case _:
            print('Incorrect tokenizeType')
    return tokenized_text

def rmStopWords(list_words, stop_words):
    list_words = [ word for word in list_words if word not in stop_words ]
    return list_words

def wordNetLemmatize(list_words):
    wnl = WordNetLemmatizer()
    list_words_lemmatized = []
    for word in list_words:
        lemmatized_word = wnl.lemmatize(word)
        list_words_lemmatized.append(lemmatized_word)
    return list_words_lemmatized

def porterStemmer(list_words):
    ps = PorterStemmer()
    list_words_stemmed = [ps.stem(word) for word in list_words]
    return list_words_stemmed

"""
    )

def sourceSentimentAnalysis():
    print(
"""
def sentimentLogReg(df, text, target):

    X_train, X_test, y_train, y_test = train_test_split(df[text], df[target], test_size = 0.2, random_state = 42)

    tfidf_vectorizer = TfidfVectorizer(max_features=1000)

    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    logreg_model = LogisticRegression(max_iter = 1000)
    logreg_model.fit(X_train_tfidf, y_train)

    y_pred = logreg_model.predict(X_test_tfidf)
    
    y_pred_test = logreg_model.predict(X_test_tfidf[4])
    print(y_pred_test)

    return X_train, X_test, y_train, y_test, logreg_model, y_pred

def sentimentRandomForest(df, text, target):

    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))

    X = vectorizer.fit_transform(df[text])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

    model_rf = RandomForestClassifier(random_state = 42)
    model_rf.fit(X_train, y_train)
    
    y_pred = model_rf.predict(X_test)

    print(model_rf.predict(X_test[4]))

    return X_train, X_test, y_train, y_test, model_rf, y_pred

"""
    )

def test():

    return None