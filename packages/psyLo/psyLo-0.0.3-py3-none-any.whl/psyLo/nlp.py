import re
import nltk
import string

from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

from nltk.stem import WordNetLemmatizer, PorterStemmer

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')


# Functions

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

# Help Functions

def help():
    print(f"""

List of Available Functions:

    Text Preprocessing:
        1.  rmExcessWhitespaces
        2.  rmHTML
        3.  rmURL
        4.  rmSpecialChar
        5.  rmPunctuation
        6.  rmNumbers
        7.  tokenize
        8.  rmStopWords
        9.  wordNetLemmatize
        10. porterStemmer
        11. example
        
1.  rmExcessWhitespaces
        parameters: text
        return value: text
          
2.  rmHTML
        parameters: text
        return value: text
          
3.  rmURL
        parameters: text
        return value: text
          
4.  rmSpecialChar
        parameters: text
        return value: text
          
5.  rmPunctuation
        parameters: text
        return value: text
          
6.  rmNumbers
        parameters: text
        return value: text
          
7.  tokenize
        parameters: text, tokenizeType = ['word', 'sentence', 'char']
        return value: list of tokens
          
8.  rmStopWords
        parameters: list of tokens
        return value: list of tokens
          
9.  wordNetLemmatize
        parameters: list of tokens
        return value: list of tokens

10. porterStemmer
        parameters: list of tokens
        return value: list of tokens

    """)

def example():
    print("\nExample: dataframe['cleanText'] = data['text'].apply(rmURL)\n")