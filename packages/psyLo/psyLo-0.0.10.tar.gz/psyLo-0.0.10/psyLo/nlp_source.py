def textPreprocessing():
    print(
"""
import re
import nltk
import time
import string
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

def numRatingsReviews(reviewPage):

    response = requests.get(reviewPage)
    soup = BeautifulSoup(response.text, 'html.parser')

    review_rating_count = soup.find('div', {'data-hook': 'cr-filter-info-review-rating-count'}).text.strip()

    numbers = re.findall(r'\b(\d{1,3}(?:,\d{3})*)\b', review_rating_count)

    num_ratings = int(numbers[0].replace(',', ''))
    num_reviews = int(numbers[1].replace(',', ''))

    print(f"\nTotal ratings: {num_ratings}\nReviews count: {num_reviews}")

    return num_ratings, num_reviews

def extractDateLocation(text):

    #date_pattern = r'\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b'

    #location_pattern = r"Reviewed in (?:the\s+)?([\w\s]+) on"

    pattern = r"Reviewed in (?:the\s+)?([\w\s]+) on (\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})"

    match = re.search(pattern, text)

    if match:
        location = match.group(1).strip()
        date = match.group(2)

    else:
        print('No date / location found')
        date = None
        location = None

    return date, location

def getReviews(url, pageNumber=None):
    
    if pageNumber:
        url += f'{pageNumber}'
    
    list_reviews = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    reviews = soup.find_all('div', {'data-hook': 'review'})
    
    for element in  reviews:

        date_location = element.find('span', {'data-hook': 'review-date'}).text.strip()

        date, location = extractDateLocation(date_location)

        dict_review = {
            'productTitle': soup.title.text.replace("Amazon.in:Customer reviews: ", ""),

            'reviewTitle': element.find('span', {'data-hook': 'review-title'}).text.strip(),

            'reviewLocation': location,

            'reviewDate': date,

            'reviewStarRating': element.find('i', {'data-hook': 'cmps-review-star-rating'}).text.strip(),
            
            'reviewBody': element.find('span', {'data-hook': 'review-body'}).text.strip()
        }

        list_reviews.append(dict_review)
        
    return list_reviews 

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

def cleanText(text):
    
    text = rmHTML(text)
    text = rmURL(text)
    text = rmSpecialChar(text)
    text = rmPunctuation(text)
    text = rmNumbers(text)

    return text

productPage = "https://www.amazon.in/Ducky-One-Mini-Pure-White/dp/B08TB2QYXX"

# making the template for the review page
reviewPage = productPage.replace('/dp/', '/product-reviews/') + "?pageNumber=" # + f"{pg}"

list_reviews = getReviews(reviewPage, 1)

df = pd.DataFrame(list_reviews)

df.to_csv('reviewsFirstPage.csv', index=False)

num_ratings, num_reviews = numRatingsReviews(reviewPage + '1')

num_pages = 1 + num_reviews // 10
list_all_reviews = []

for i in range(num_pages):

    try:
        list_all_reviews = list_all_reviews + getReviews(reviewPage, i+1)
        # time.sleep(5)
        
    except Exception as error:
        print(f'\nERROR: Iteration: {i}: {error}')

data = pd.read_csv('reviewsFirstPage.csv')

df['reviewBody_cleaned'] = df['reviewBody'].apply(cleanText)
df['reviewTitle_cleaned'] = df['reviewTitle'].apply(cleanText)

def tokenize(text, tokenizeType='word'):

    match tokenizeType:
        case 'word':
            tokenized_text = word_tokenize(text.lower())

        case 'sentence':
            tokenized_text = sent_tokenize(text.lower())

        case 'char':
            tokenizer = RegexpTokenizer(r'\w')
            tokenized_text = tokenizer.tokenize(text)
            
        case _:
            print('Incorrect tokenizeType')

    return tokenized_text

list_tokenizeType = ['word', 'sentence', 'char']

sample_text = df['reviewBody_cleaned'][0]

for tokenizeType in list_tokenizeType:

    tokenized_sample = tokenize(sample_text, tokenizeType)
    
    print(f'\n\nTokenized by: {tokenizeType}\n\n{tokenized_sample}')

def rmStopWords(list_words, stop_words):
        
    list_words = [ word for word in list_words if word not in stop_words ]

    return list_words

stop_words = set(stopwords.words('english'))

sample_text = df['reviewBody_cleaned'][0]

tokenized_sample = tokenize(sample_text, 'word')

tokenized_sample_no_stopwords = rmStopWords(tokenized_sample, stop_words)

print(tokenized_sample_no_stopwords)

sample = tokenized_sample_no_stopwords

porter_stemmer = PorterStemmer()

tokenized_sample_no_stopwords_stemmed = [porter_stemmer.stem(word) for word in sample]

print(tokenized_sample_no_stopwords_stemmed)

def wordNetLemmatize(list_words):

    wnl = WordNetLemmatizer()

    list_words_lemmatized = []

    for word in list_words:

        lemmatized_word = wnl.lemmatize(word)

        list_words_lemmatized.append(lemmatized_word)

    return list_words_lemmatized

tokenized_sample_no_stopwords_lemmatized = wordNetLemmatize(sample)

print(tokenized_sample_no_stopwords_lemmatized)
"""
    )
    return None

def entityExtraction():
    print(
"""
import re
import spacy
from spacy import displacy

def checkHex(text):

    pattern = r'#(?:[0-9a-fA-F]{3}){1,2}\b'
    
    result = re.findall(pattern, text)

    return result

input_string = "#zaw881, aaa, #aef002, #AEK320, #aBC, #00000A, #ac9, acz011"

valid_colors = checkHex(input_string)

print("Valid Hex Colors:")

for color in valid_colors:
    print(color)

spacy.cli.download("en_core_web_sm")

nlp = spacy.load("en_core_web_sm")

text = "Founded in 2004, Facebook is headquartered in California."

doc = nlp(text)

# defining a dictionary for color coded visualization
options = {"ents": ["DATE", "ORG", "GPE"], "colors": {"DATE": "#FFA07A", "ORG": "#98FB98", "GPE": "#87CEFA"}}


text_vis = displacy.render(doc, style = "ent", options = options, page = False)

print(f'\nNamed Entity Recognition Results:\n{text_vis}')

print("\nEntities found:")
for ent in doc.ents:
    print(f'{ent.text} - {ent.label_}')

text = '''Kiran want to know the famous foods in each state of India. So, he opened Google and search for this question. Google showed that in Delhi it is Chaat, in Gujarat it is Dal Dhokli, in Rajasthan it is dal baati, in Andhrapradesh it is Biryani, in Assam it is Papaya Khar, in Bihar it is Litti Chowkha, in Maharashtra it is Misal and so on for all other states.'''

doc = nlp(text)

print('\nGPEs (Geopolitical Entities) found in the input are:')
for ent in doc.ents:
    if ent.label_ == "GPE":
        print(f'\n  {ent.text}')

text = "Once upon a time, Rohan won many medals for his school."
doc = nlp(text)

# printing the POS, Tag, Dependency
for token in doc:
    print(f'{token.text:<12} POS: {token.pos_:<6} Tag: {token.tag_:<6} Dep: {token.dep_}')

print("\nDependency Parse Visualization:")

# visual parameters
options = {"compact": True, "font": "Arial", "bg": "#ffffff"}

dependency_vis = displacy.render(doc, style = "dep", options = options, page = False)

print(dependency_vis)
"""
    )
    return None

def featureEngineering():
    print(
"""
import pandas as pd
data = pd.read_csv('main.csv', index_col = 0)
data = data.iloc[:1000]

# Bag of Words
from sklearn.feature_extraction.text import CountVectorizer

vectorizer_bow = CountVectorizer()
X_bow = vectorizer_bow.fit_transform(data['cleaned_text'])

# tfidf
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer_tfidf = TfidfVectorizer()
X_tfidf = vectorizer_tfidf.fit_transform(data['cleaned_text'])

# word2vec
from gensim.models import Word2Vec
import numpy as np

tokenized_texts = [text.split() for text in data['cleaned_text']]

model_w2v = Word2Vec(tokenized_texts, vector_size=100, window=5, min_count=1)

def vectorize_w2v(text):
    words = text.split()
    word_vecs = [model_w2v.wv[word] for word in words if word in model_w2v.wv]
    return np.mean(word_vecs, axis=0) if word_vecs else np.zeros(model_w2v.vector_size)

X_w2v = np.array([vectorize_w2v(text) for text in data['cleaned_text']])

# fast text
from gensim.models import FastText

model_ft = FastText(tokenized_texts, vector_size=100, window=5, min_count=1)

def vectorize_ft(text):
    words = text.split()
    word_vecs = [model_ft.wv[word] for word in words if word in model_ft.wv]
    return np.mean(word_vecs, axis=0) if word_vecs else np.zeros(model_ft.vector_size)

X_ft = np.array([vectorize_ft(text) for text in data['cleaned_text']])

# eval
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

def evaluate_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    
    return accuracy, f1

# Evaluate each feature engineering technique
results = {}

# BoW
results['BoW'] = evaluate_model(X_bow.toarray(), data['polarity'])

# TF-IDF
results['TF-IDF'] = evaluate_model(X_tfidf.toarray(), data['polarity'])

# Word2Vec
results['Word2Vec'] = evaluate_model(X_w2v, data['polarity'])

# FastText
results['FastText'] = evaluate_model(X_ft, data['polarity'])

print("Evaluation Results:")
for method, (accuracy, f1) in results.items():
    print(f"{method} - Accuracy: {accuracy:.4f}, F1-Score: {f1:.4f}")
"""
    )
    return None

def nlpApplications():
    print(
"""
# Topic Modeling
import re
import nltk
import pandas as pd
from gensim import corpora
from nltk.corpus import stopwords
from gensim.models import LdaModel
from nltk.tokenize import word_tokenize

def preprocess_text(text):

    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    return tokens

def map_topic_to_category(topic_num):
    topic_mapping = {
        2: 'Business',
        1: 'Entertainment',
        5: 'Politics',
        3: 'Sport',
        4: 'Tech'
    }
    
    return topic_mapping.get(topic_num, 'Unknown')

def perform_topic_modeling(csv_file, num_topics=5):

    df = pd.read_csv(csv_file)

    df['combined_text'] = df['Title'] + ' ' + df['Description']

    df['processed_text'] = df['combined_text'].apply(preprocess_text)

    dictionary = corpora.Dictionary(df['processed_text'])

    corpus = [dictionary.doc2bow(text) for text in df['processed_text']]

    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42)

    def get_dominant_topic(bow):
        return max(lda_model[bow], key=lambda x: x[1])[0]
    
    df['topic_num'] = [get_dominant_topic(bow) for bow in corpus]

    df['topic_category'] = df['topic_num'].apply(map_topic_to_category)

    output_file = 'output_with_topics.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Topic modeling completed. Results saved to {output_file}")

    print("\nTopics:")
    for idx, topic in lda_model.print_topics(-1):
        print(f"\nTopic {idx+1}: {topic}")
        print(f"\nMapped Category: {map_topic_to_category(idx+1)}")
        print()

perform_topic_modeling('news_articles.csv', num_topics=5)




# Sentiment Analysis
# kaggle datasets download -d kritanjalijain/amazon-reviews
import re
import string
import numpy as np
import pandas as pd
import contractions
import matplotlib.pyplot as plt

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

columns = ['polarity', 'title', 'text']

train = pd.read_csv('./data/train.csv', names = columns, header = None)
# test  = pd.read_csv('./data/test.csv', names = columns, header = None)

print(train.value_counts('polarity'))

def expand_contractions(text):
    result = ' '.join(contractions.fix(word) for word in text.split())

    return result

def expand_contractions_batch(texts):
    expanded_texts = []
    for text in texts:
        expanded_texts.append(' '.join(contractions.fix(word) for word in text.split()))
        
    return expanded_texts

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

def cleanText(text):
    
    text = expand_contractions(text)

    text = rmHTML(text)
    text = rmURL(text)

    text = rmSpecialChar(text)
    text = rmPunctuation(text)

    text = rmNumbers(text)

    text = text.lower()

    return text

stopwords=stopwords.words('english')
lemmatizer = WordNetLemmatizer()

def preprocessText(text):

    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    cleaned_text = ' '.join(filtered_words) 
    
    return cleaned_text

train['cleaned_text'] = train['text'].apply(cleanText)

train['cleaned_text'] = train['cleaned_text'].apply(preprocessText)

train.to_csv('main.csv')

data = train.iloc[:1000]

def sentimentAnalysis(data, text_column):

    vec = TfidfVectorizer(encoding="latin-1", strip_accents="unicode")
    features = vec.fit_transform(data[text_column]) 
    
    # Creating target variable (1 for negative, 2 for positive)
    # and map polarity to sentiment labels
    y = np.where(data['polarity'] == 1, 'Negative', 'Positive')  

    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test, train_indices, test_indices = train_test_split(
        features, y, np.arange(len(data)), test_size=0.2, random_state=44)

    # Hyperparameter tuning with GridSearchCV
    param_grid = {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf'],
        'gamma': ['scale', 'auto']
    }
    
    grid_search = GridSearchCV(SVC(probability=True), param_grid, cv=5)
    # Enable probability estimates
    grid_search.fit(X_train, y_train)

    # Best parameters from Grid Search
    print("Best Parameters:", grid_search.best_params_)

    # Train the model with best parameters
    best_model = grid_search.best_estimator_
    best_model.fit(X_train, y_train)

    # Make predictions on the test set
    svm_prediction = best_model.predict(X_test)
    
    # Get probabilities for predictions
    probabilities = best_model.predict_proba(X_test)

    # Determine sentiment labels based on predictions and probabilities
    sentiment_labels = []
    
    for prob in probabilities:
        if prob[0] > 0.7:  # High confidence negative
            sentiment_labels.append('Negative')
        elif prob[1] > 0.7:  # High confidence positive
            sentiment_labels.append('Positive')
        else:
            sentiment_labels.append('Neutral')  # Uncertain predictions

    # Accuracy score
    print("Accuracy:", accuracy_score(y_test, svm_prediction))

    # Create a new column in the DataFrame for predictions using original indices
    data['sentiment'] = 'Neutral'  # Default to Neutral for all rows initially
    data.loc[test_indices, 'sentiment'] = sentiment_labels

    return data[['cleaned_text', 'sentiment']]

sentimentAnalysis(data, 'cleaned_text')

#Best Parameters: {'C': 10, 'gamma': 'scale', 'kernel': 'rbf'}
#Accuracy: 0.835
"""
    )
    return None

def realTimeApplications(type):
    
    match(type):
        case 'docSearch':
            print(
"""
# Document Search
import spacy
import numpy as np, pandas as pd
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer

from langchain.text_splitter import CharacterTextSplitter

main = pd.read_csv('main_dataframe.csv')

def fetchTopIndices(array, k):

    kth_largest = (k + 1) * -1

    result = np.argsort(array)[:kth_largest:-1]
    
    return result

def docSearch(text, query):

    nlp = spacy.load('en_core_web_sm')
    vectorizer = TfidfVectorizer(stop_words='english')

    tokens = sent_tokenize(text)
    features = vectorizer.fit_transform(tokens)

    query_tfidf = vectorizer.transform(query)

    cosine_similarities = cosine_similarity(features, query_tfidf).flatten()

    top_indices = fetchTopIndices(cosine_similarities, 3)

    for i in range(len(top_indices)):
        print(tokens[top_indices[i]])

text_sample = main['cleaned_text'][0]
docSearch(text_sample, ['who is snow white?'])

def initTextSplitter(separator = '.', chunk_size = 300, chunk_overlap = 50, length_function = len):
    
    text_splitter = CharacterTextSplitter(
        separator = separator,
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = length_function
    )

    return text_splitter

def chunkEmbed(text):

    text_splitter = initTextSplitter()

    chunked_text = text_splitter.split_text(text)

    encoder = TfidfVectorizer(analyzer = 'word', max_features = 10000, ngram_range = (1,3), norm = 'l2')

    chunk_embeddings = encoder.fit_transform(chunked_text).toarray()

    ids = range(len(chunked_text))

    raw_text_embeddings_dict = {i:{'text': text, 'embedding': embedding} for i, text, embedding in zip(ids, chunked_text, chunk_embeddings)}

    return raw_text_embeddings_dict, encoder

raw_text_embeddings_dict, encoder = chunkEmbed(text_sample)

def topAnswers(raw_text_embeddings_dict, query, encoder, num_answers = 2):

    query_embedding = encoder.transform([query])
    
    distance_scores = []

    for _, text_embed in raw_text_embeddings_dict.items():

        chunk_embedding = text_embed['embedding'].reshape(1, -1)

        score = euclidean_distances(chunk_embedding, query_embedding.reshape(1, -1))[0][0]
        
        distance_scores.append(score)
        
    # Top 3 lowest scores representing top 3 similar chunks
    top_texts = sorted(enumerate(distance_scores), key = lambda x: x[1])[:num_answers]
    
    n = 0
    for sim_doc in top_texts:
        n += 1

        sim_index = sim_doc[0]

        print(f"\n\nSimilarChunk {str(n)} \n\n{raw_text_embeddings_dict[sim_index]['text']}")

question = 'what did the queen hear the mirror say?'
print(topAnswers(raw_text_embeddings_dict, question, encoder, 5))
"""
    )
        case 'sumWordCloud':
            print(
"""
import re
import fitz
import pandas as pd

document = fitz.open('Story_Book.pdf')

def rmExcessNewlines(text):

    text = re.sub(r'(\s*\n\s*)+', '\n', text)

    return text

def rmTags(text):

    rmTags_pattern = re.compile(r'© 2012 Tantor Media,|Inc\. © 2012 Tantor Media,|Inc\. © 2012 Tantor')

    text = re.sub(rmTags_pattern, '', text)
    
    return text

data = []

for page_no in range(len(document)):
    text = document[ page_no ].get_text()
    
    cleaned_text = rmTags(text)

    cleaned_text = rmExcessNewlines(cleaned_text)

    data.append({'text': cleaned_text})

dataframe = pd.DataFrame(data)

temp_text = dataframe['text'][2]

contents_index = temp_text.find('Contents')

if contents_index != -1:
    contents = temp_text[contents_index + len('Contents'):].strip()
    
    titles = [title.strip() for title in contents.split('\n') if title.strip()]

else:
    titles = []

print(titles)

def isTitlePage(page_content):
    
    title_page_pattern = r'^\s*\d+\s*\n\s*([A-Z][A-Za-z\s]+)\s*\n?$'

    result = re.match(title_page_pattern, page_content, re.MULTILINE)
    
    return result

def extractTitle(match):

    title = match.group(1).strip()

    return title

def isKnownTitle(title, title_list):

    result = any(known_title.lower() == title.lower() for known_title in title_list)

    return result

def addStory(stories, current_title, current_text):

    if current_title and current_text:
        stories.append({"title": current_title, "text": current_text.strip()})

    return None

def extractStories(df, title_list):
    
    stories = []

    current_title = ""
    current_text = ""
    
    for _, row in df.iterrows():

        page_content = row['text']

        title_match = isTitlePage(page_content)
        
        if title_match:
            potential_title = extractTitle(title_match)
            
            if isKnownTitle(potential_title, title_list):
                addStory(stories, current_title, current_text)
                current_title = potential_title
                current_text = ""
            else:
                current_text += page_content + "\n"
        else:
            current_text += page_content + "\n"
    
    addStory(stories, current_title, current_text)
    
    return pd.DataFrame(stories)

main = extractStories(dataframe, titles)

main.to_csv('story_book_main.csv')

import string

def rmExcessWhitespaces(text):

    text = re.sub(r'\s+', ' ', text).strip()

    return text

def rmSpecialChar(text):

    rmSpecialChar_pattern = re.compile(r'[^a-zA-Z0-9\s]')

    text = re.sub(rmSpecialChar_pattern, '', text)

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

def cleanText(text):

    # text = rmSpecialChar(text)
    # text = rmPunctuation(text)
    text = rmNumbers(text)
    # text = text.lower()

    return text

main['cleaned_text'] = main['text'].apply(cleanText)

# Extractive Summary

import spacy
from heapq import nlargest
from string import punctuation
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS

def getWordFrequencies(doc, stopwords, punctuation):

    word_frequencies = {}

    for word in doc:
        if word.text.lower() not in stopwords: 
            if word.text.lower() not in punctuation: 
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1 
                else:
                    word_frequencies[word.text] += 1

    return word_frequencies 

def normalizeWordFrequencies(word_frequencies):

    maxFrequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/maxFrequency

    return word_frequencies

def getSentTokens(doc):

    sent_tokens = [sent for sent in doc.sents]

    return sent_tokens

def getSentScores(sent_tokens, word_frequencies):

    sent_scores = {}  

    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sent_scores[sent] += word_frequencies[word.text.lower()]

    return sent_scores

def extractiveSummary(text, summary_percentage = 0.1):
    
    # python -m spacy download en_core_web_sm
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    stopwords = list(STOP_WORDS)
    
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n'

    word_frequencies = getWordFrequencies(doc, stopwords, punctuation)

    normalized_word_frequencies = normalizeWordFrequencies(word_frequencies)
    
    sent_tokens = getSentTokens(doc)

    sent_scores = getSentScores(sent_tokens, normalized_word_frequencies)

    num_summary_sentences = int(len(sent_scores) * summary_percentage)

    summary = nlargest(num_summary_sentences, sent_scores, key=sent_scores.get)

    summary = [word.text for word in summary]

    summary = ''.join(summary)

    return summary

# Alternative
'''    
    # calaculate word frequencies
    words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(words)
    
    # normalizing frequencies
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] /= max_freq
    
    # sentence scores
    sentence_scores = {}
    for sent in doc.sents:

        for word in sent:

            if word.text.lower() in word_freq:

                if sent not in sentence_scores:
                    sentence_scores[sent] = 0
                sentence_scores[sent] += word_freq[word.text.lower()]
    
    # determining the number of sentences to include based on a percentage that is 0.1 by default (if nothing is passed to the function)
    num_sentences = len(list(doc.sents))

    # max function to ensure that at least one sentence is selected
    num_summary_sentences = max(1, int(num_sentences * summary_percentage))  
    
    # selecting the sentences from the top scores
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_summary_sentences]
    
    summary = ' '.join([sent.text for sent in summarized_sentences])

    return summary
'''

main['extractiveSummary'] = main['cleaned_text'].apply(extractiveSummary)

# Abstractive Summary
# bart
def bartAbstractiveSummary(text):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    input = tokenizer.encode(text, return_tensors="pt", max_length=512)

    summary_ids = model.generate(input, max_length=300, min_length=200, length_penalty=1.0, num_beams=4)

    summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]

    return summary

main['bartAbstractiveSummary'] = main['cleaned_text'].apply(bartAbstractiveSummary)

# Word Cloud

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def wordCloud(text):
    nlp = spacy.load('en_core_web_sm')

    stop_words = set(stopwords.words('english'))

    #tokenize
    word_tokens = word_tokenize(text)

    # rm alphanumerics
    word_tokens = [word for word in word_tokens if word.isalnum()]

    word_tokens = [word for word in word_tokens if not word.lower() in stop_words]

    word_tokens = ' '.join(word_tokens)

    doc = nlp(word_tokens)
    doc = [token.lemma_ for token in doc]

    result = ' '.join(doc)

    wordCloud = WordCloud(collocations = False, width = 1920, height = 1080).generate(result)

    plt.imshow(wordCloud, interpolation = 'bilinear')
    plt.axis("off")
    plt.show()

main['cleaned_text'].apply(wordCloud)

main.to_csv('main_dataframe.csv')
"""
            )
    return None

def langChain():
    print(
'''
# -*- coding: utf-8 -*-
"""1.6 LCEL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13bWyeatfg6UyxXlEFX5KSDofIGK_q44Z
"""

from google.colab import userdata

# Get the API key from user secrets using the correct name
api_key = userdata.get('GOOGLE_API_KEY_1')

import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

from langchain_core.messages import HumanMessage,SystemMessage

messages=[
    SystemMessage(content="Translate the following from English to French"),
    HumanMessage(content="Hey!")
]
# Prepare the prompt for the Google Generative AI model
prompt = messages[0].content + " " + messages[1].content

# Generate the response using generate_content() instead of generate_text()
result = model.generate_content(prompt)

print(result.text)  # Print the generated text

result

result.text

"""## StrOutputParser"""

from langchain_core.output_parsers import StrOutputParser
parser=StrOutputParser()
parser.invoke(result.text)

"""## LCEL"""

from langchain_google_genai import GoogleGenerativeAI

# Initialize the model
api_key = api_key  # Replace with your actual API key
llm = GoogleGenerativeAI(api_key=api_key, model="gemini-pro")

# Directly invoke the model with a string
response = llm.invoke("What is the capital of France?")
print(response)

from langchain_core.runnables import RunnablePassthrough

def format_input(input_dict):
    # Extract plain string input
    return input_dict["input"][0]["content"]

# Test the formatter
input_data = {"input": [{"content": "What is the capital of France?", "role": "user"}]}
formatted_input = format_input(input_data)
print(formatted_input)  # Should print: "What is the capital of France?"

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import HumanMessage

llm = GoogleGenerativeAI(api_key=api_key, model="gemini-pro")

# Define the input formatter function to format the input correctly
def format_input(input_dict):
    # Ensure the input is passed as a list of HumanMessage
    user_message = input_dict["input"][0]["content"]
    return [HumanMessage(content=user_message)]  # Return list of BaseMessages (HumanMessage)

# Define the RunnablePassthrough to apply the format_input transformation
runnable_formatter = RunnablePassthrough(assign=format_input)

# Chain the formatter with the model
chain = runnable_formatter | llm

# Define the input data as a dictionary containing messages
input_data = {"input": [{"content": "What is the capital of France?", "role": "user"}]}

# Now, pass the correctly formatted input to the chain
formatted_input = format_input(input_data)

# Invoke the chain with the formatted input
result = chain.invoke(formatted_input)
print(result)  # Print the result of the model's response

### Using LCEL- chain the components
chain=llm|parser
chain.invoke(messages)

"""## Prompt Templates"""

### Prompt Templates
from langchain_core.prompts import ChatPromptTemplate

generic_template="Trnaslate the following into {language}:"

prompt=ChatPromptTemplate.from_messages(
    [("system",generic_template),("user","{text}")]
)

result=prompt.invoke({"language":"French","text":"Hello"})

result.to_messages()

##Chaining together components with LCEL
chain=prompt|llm|parser
chain.invoke({"language":"French","text":"Hello"})

'''
    )
    return None

def textSummarization():
    print(
'''
# -*- coding: utf-8 -*-
"""1.7 text_summarization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1K2eMaUVsBTe9TAc-UzeByzVd3ekgKcXT

# Text Summarization
"""

!pip install python-dotenv

from google.colab import userdata

# Get the API key from user secrets using the correct name
api_key = userdata.get('GOOGLE_API_KEY_1')

import google.generativeai as genai

genai.configure(api_key=api_key)
llm = genai.GenerativeModel('gemini-pro')

from langchain.schema import(
    AIMessage,
    HumanMessage,SystemMessage
)

speech="""
People across the country, involved in government, political, and social activities, are dedicating their time to make the ‘Viksit Bharat Sankalp Yatra’ (Developed India Resolution Journey) successful. Therefore, as a Member of Parliament, it was my responsibility to also contribute my time to this program. So, today, I have come here just as a Member of Parliament and your ‘sevak’, ready to participate in this program, much like you.

In our country, governments have come and gone, numerous schemes have been formulated, discussions have taken place, and big promises have been made. However, my experience and observations led me to believe that the most critical aspect that requires attention is ensuring that the government’s plans reach the intended beneficiaries without any hassles. If there is a ‘Pradhan Mantri Awas Yojana’ (Prime Minister’s housing scheme), then those who are living in jhuggis and slums should get their houses. And he should not need to make rounds of the government offices for this purpose. The government should reach him. Since you have assigned this responsibility to me, about four crore families have got their ‘pucca’ houses. However, I have encountered cases where someone is left out of the government benefits. Therefore, I have decided to tour the country again, to listen to people’s experiences with government schemes, to understand whether they received the intended benefits, and to ensure that the programs are reaching everyone as planned without paying any bribes. We will get the real picture if we visit them again. Therefore, this ‘Viksit Bharat Sankalp Yatra’ is, in a way, my own examination. I want to hear from you and the people across the country whether what I envisioned and the work I have been doing aligns with reality and whether it has reached those for whom it was meant.

It is crucial to check whether the work that was supposed to happen has indeed taken place. I recently met some individuals who utilized the Ayushman card to get treatment for serious illnesses. One person met with a severe accident, and after using the card, he could afford the necessary operation, and now he is recovering well. When I asked him, he said: “How could I afford this treatment? Now that there is the Ayushman card, I mustered courage and underwent an operation. Now I am perfectly fine.”  Such stories are blessings to me.

The bureaucrats, who prepare good schemes, expedite the paperwork and even allocate funds, also feel satisfied that 50 or 100 people who were supposed to get the funds have got it. The funds meant for a thousand villages have been released. But their job satisfaction peaks when they hear that their work has directly impacted someone’s life positively. When they see the tangible results of their efforts, their enthusiasm multiplies. They feel satisfied. Therefore, ‘Viksit Bharat Sankalp Yatra’ has had a positive impact on government officers. It has made them more enthusiastic about their work, especially when they witness the tangible benefits reaching the people. Officers now feel satisfied with their work, saying, “I made a good plan, I created a file, and the intended beneficiaries received the benefits.” When they find that the money has reached a poor widow under the Jeevan Jyoti scheme and it was a great help to her during her crisis, they realise that they have done a good job. When a government officer listens to such stories, he feels very satisfied.

There are very few who understand the power and impact of the ‘Viksit Bharat Sankalp Yatra’. When I hear people connected to bureaucratic circles talking about it, expressing their satisfaction, it resonates with me. I’ve heard stories where someone suddenly received 2 lakh rupees after the death of her husband, and a sister mentioned how the arrival of gas in her home transformed her lives. The most significant aspect is when someone says that the line between rich and poor has vanished. While the slogan ‘Garibi Hatao’ (Remove Poverty) is one thing, but the real change happens when a person says, “As soon as the gas stove came to my house, the distinction between poverty and affluence disappeared.
"""

speech

chat_message=[
    SystemMessage(content="You are expert with experise in summarizing speeched"),
    HumanMessage(content=f"Please provide a short and concisse summary of the follow speech:\n Text:{speech}")
]

dir(llm)  # This will list all the available methods and attributes of the llm object

llm.count_tokens(speech)

"""## Prompt Template Text Summarization"""

from langchain.chains import LLMChain
from langchain import PromptTemplate

generictemplate="""
Write a summary of the following speech:
Speech:{speech}
Translate the precise summary to {language}
"""

prompt=PromptTemplate(
    input_variables=['speech','language'],
    template=generictemplate
)
prompt

complete_prompt=prompt.format(speech=speech,language="French")
complete_prompt

llm.count_tokens(complete_prompt)

!pip install langchain_google_genai

from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain import PromptTemplate

llm = GoogleGenerativeAI(model="gemini-pro", temperature=0, api_key=api_key)
llm_chain = LLMChain(llm=llm, prompt=prompt)
summary=llm_chain.run({'speech':speech,'language':'hindi'})
summary

"""## StuffDocumentChain Text summarization"""

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("/content/apjspeech.pdf")
docs = loader.load_and_split()
docs[0]

template=""" Write a concise and short summary of the following speech,
Speech :{text}

 """
prompt=PromptTemplate(input_variables=['text'],
                      template=template)

from langchain.chains.summarize import load_summarize_chain

chain=load_summarize_chain(llm,chain_type='stuff',prompt=prompt,verbose=True)
output_summary=chain.run(docs)
output_summary

"""### Map reduce to Summarize Large documents"""

from langchain.text_splitter import RecursiveCharacterTextSplitter

# docs

final_documents=RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=100).split_documents(docs)
final_documents[0]

len(final_documents)

chunks_prompt="""
Please summarize the below speech:
Speech:`{text}'
Summary:
"""
map_prompt_template=PromptTemplate(input_variables=['text'],
                                    template=chunks_prompt)

final_prompt="""
Provide the final summary of the entire speech with these important points.
Add a Motivation Title,Start the precise summary with an introduction and provide the summary in number
points for the speech.
Speech:{text}

"""
final_prompt_template=PromptTemplate(input_variables=['text'],template=final_prompt)
final_prompt_template

summary_chain=load_summarize_chain(
    llm=llm,
    chain_type="map_reduce",
    map_prompt=map_prompt_template,
    combine_prompt=final_prompt_template,
    verbose=True
)

output=summary_chain.run(final_documents)
output

"""### Refine Chain For Summarization"""

chain=load_summarize_chain(
    llm=llm,
    chain_type="refine",
    verbose=True
)
output_summary=chain.run(final_documents)
output_summary

'''
    )
    return None

def help():
    print(
"""
Available:

    textPreprocessing()
    entityExtraction()
    featureEngineering()
    nlpApplications()
    realTimeApplications(type= 'docSearch', 'sumWordCloud')
    langChain()
    textSummarization()
    help
"""
    )
    return None