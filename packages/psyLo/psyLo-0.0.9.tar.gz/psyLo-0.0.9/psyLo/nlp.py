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
install('tensorflow')

import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

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

# Data Sentiment Analysis

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

# Text Generation

def textGeneration(text, seed_text, length=100):

    # Lowercase and remove special characters
    text = text.lower().replace("\n", " ")

    # Create a character-to-index mapping
    chars = sorted(list(set(text)))
    char_to_idx = {char: idx for idx, char in enumerate(chars)}
    idx_to_char = {idx: char for char, idx in char_to_idx.items()}

    print(f"Unique characters: {chars}")
    print(f"Total unique characters: {len(chars)}")

    # Sequence length
    SEQ_LENGTH = 40

    # Prepare input and output sequences
    input_sequences = []
    output_chars = []

    for i in range(len(text) - SEQ_LENGTH):
        input_seq = text[i:i + SEQ_LENGTH]
        output_char = text[i + SEQ_LENGTH]
        input_sequences.append([char_to_idx[char] for char in input_seq])
        output_chars.append(char_to_idx[output_char])

    # Convert to NumPy arrays
    input_sequences = np.array(input_sequences)
    output_chars = np.array(output_chars)

    print("Input shape:", input_sequences.shape)
    print("Output shape:", output_chars.shape)

    # Define model
    model = Sequential([
        Embedding(input_dim=len(chars), output_dim=50, input_length=SEQ_LENGTH),
        LSTM(256, return_sequences=False),
        Dense(len(chars), activation="softmax")
    ])

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")
    model.summary()

    # Train the model
    model.fit(input_sequences, output_chars, epochs=30, batch_size=128)

    # Convert seed text to indices
    input_seq = [char_to_idx[char] for char in seed_text.lower()]

    # Generate text
    generated_text = seed_text

    for _ in range(length):
        # Pad the sequence to the required length
        input_seq_padded = np.pad(input_seq, (SEQ_LENGTH - len(input_seq), 0), mode='constant')[-SEQ_LENGTH:]
        input_seq_padded = np.expand_dims(input_seq_padded, axis=0)

        # Predict the next character
        predictions = model.predict(input_seq_padded, verbose=0)
        next_char_idx = np.argmax(predictions)
        next_char = idx_to_char[next_char_idx]

        # Append the character to the text
        generated_text += next_char
        input_seq.append(next_char_idx)

    return generated_text

# Seq2Seq

def seq2seq(path):

    # Read the dataset file
    data_file = path  # Example file: English-Marathi
    pairs = []

    # Load data and preprocess
    with open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                pairs.append((parts[0].strip().lower(), parts[1].strip().lower()))

    df = pd.DataFrame(pairs, columns=["source", "target"])
    print("Sample Data:\n", df.head())
    
    # Add start and end tokens to target language
    df['target'] = df['target'].apply(lambda x: f"<start> {x} <end>")

    # Tokenization
    source_tokenizer = Tokenizer(filters='')
    target_tokenizer = Tokenizer(filters='')

    source_tokenizer.fit_on_texts(df['source'])
    target_tokenizer.fit_on_texts(df['target'])

    source_sequences = source_tokenizer.texts_to_sequences(df['source'])
    target_sequences = target_tokenizer.texts_to_sequences(df['target'])

    source_vocab_size = len(source_tokenizer.word_index) + 1
    target_vocab_size = len(target_tokenizer.word_index) + 1
    
    # Pad sequences
    max_source_len = max(len(seq) for seq in source_sequences)
    max_target_len = max(len(seq) for seq in target_sequences)

    source_sequences = pad_sequences(source_sequences, maxlen=max_source_len, padding='post')
    target_sequences = pad_sequences(target_sequences, maxlen=max_target_len, padding='post')

    # Split data into training and validation
    train_size = int(0.8 * len(source_sequences))
    X_train, X_val = source_sequences[:train_size], source_sequences[train_size:]
    y_train, y_val = target_sequences[:train_size], target_sequences[train_size:]

    # Model parameters
    embedding_dim = 256
    units = 512
    
    # Encoder
    class Encoder(tf.keras.Model):
        def __init__(self, vocab_size, embedding_dim, enc_units):
            super(Encoder, self).__init__()
            self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
            self.lstm = tf.keras.layers.LSTM(enc_units, return_sequences=True, return_state=True)

        def call(self, x):
            x = self.embedding(x)
            output, state_h, state_c = self.lstm(x)
            return output, state_h, state_c

    # Decoder
    class Decoder(tf.keras.Model):
        def __init__(self, vocab_size, embedding_dim, dec_units):
            super(Decoder, self).__init__()
            self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
            self.lstm = tf.keras.layers.LSTM(dec_units, return_sequences=True, return_state=True)
            self.fc = tf.keras.layers.Dense(vocab_size, activation='softmax')

        def call(self, x, enc_output, states):
            x = self.embedding(x)
            output, state_h, state_c = self.lstm(x, initial_state=states)
            x = self.fc(output)
            return x, state_h, state_c

    # Create encoder and decoder
    encoder = Encoder(source_vocab_size, embedding_dim, units)
    decoder = Decoder(target_vocab_size, embedding_dim, units)

    # Optimizer and loss
    optimizer = tf.keras.optimizers.Adam()
    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False, reduction='none')

    def loss_function(real, pred):
        mask = tf.math.logical_not(tf.math.equal(real, 0))
        loss = loss_object(real, pred)
        mask = tf.cast(mask, dtype=loss.dtype)
        loss *= mask
        return tf.reduce_mean(loss)

    # Training step
    @tf.function
    def train_step(source, target_in, target_out):
        loss = 0
        with tf.GradientTape() as tape:
            enc_output, enc_h, enc_c = encoder(source)
            dec_h, dec_c = enc_h, enc_c
            dec_input = target_in[:, 0:1]  # Start with the <start> token

            for t in range(1, target_out.shape[1]):
                predictions, dec_h, dec_c = decoder(dec_input, enc_output, [dec_h, dec_c])
                loss += loss_function(target_out[:, t], predictions)
                dec_input = tf.expand_dims(target_out[:, t], 1)

        batch_loss = loss / int(target_out.shape[1])
        variables = encoder.trainable_variables + decoder.trainable_variables
        gradients = tape.gradient(loss, variables)
        optimizer.apply_gradients(zip(gradients, variables))
        return batch_loss

    # Prepare data for training
    BATCH_SIZE = 64
    BUFFER_SIZE = len(X_train)
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
    val_dataset = tf.data.Dataset.from_tensor_slices((X_val, y_val)).batch(BATCH_SIZE)

    # Training loop
    EPOCHS = 10
    for epoch in range(EPOCHS):
        total_loss = 0
        for (batch, (source, target)) in enumerate(train_dataset):
            target_in = target[:, :-1]
            target_out = target[:, 1:]
            batch_loss = train_step(source, target_in, target_out)
            total_loss += batch_loss

        print(f"Epoch {epoch + 1}, Loss: {total_loss / batch}")

    return None

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
    
    Text Generation:
        15. textGeneration(text, seed_text, length=100)
        
        Returns the generated text
    
    Seq2Seq:
        16. seq2seq(path_to_data)

    Print Source:
        1. sourceTextPreprocessing()
        2. sourceSentimentAnalysis()
        3. sourceTextGeneration()
        4. sourceSeq2seq()
        5. sourceImports()
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

def sourceTextGeneration():
    print(
"""
# Text Generation

def textGeneration(text, seed_text, length=100):

    # Lowercase and remove special characters
    text = text.lower().replace("\n", " ")

    # Create a character-to-index mapping
    chars = sorted(list(set(text)))
    char_to_idx = {char: idx for idx, char in enumerate(chars)}
    idx_to_char = {idx: char for char, idx in char_to_idx.items()}

    print(f"Unique characters: {chars}")
    print(f"Total unique characters: {len(chars)}")

    # Sequence length
    SEQ_LENGTH = 40

    # Prepare input and output sequences
    input_sequences = []
    output_chars = []

    for i in range(len(text) - SEQ_LENGTH):
        input_seq = text[i:i + SEQ_LENGTH]
        output_char = text[i + SEQ_LENGTH]
        input_sequences.append([char_to_idx[char] for char in input_seq])
        output_chars.append(char_to_idx[output_char])

    # Convert to NumPy arrays
    input_sequences = np.array(input_sequences)
    output_chars = np.array(output_chars)

    print("Input shape:", input_sequences.shape)
    print("Output shape:", output_chars.shape)

    # Define model
    model = Sequential([
        Embedding(input_dim=len(chars), output_dim=50, input_length=SEQ_LENGTH),
        LSTM(256, return_sequences=False),
        Dense(len(chars), activation="softmax")
    ])

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")
    model.summary()

    # Train the model
    model.fit(input_sequences, output_chars, epochs=30, batch_size=128)

    # Convert seed text to indices
    input_seq = [char_to_idx[char] for char in seed_text.lower()]

    # Generate text
    generated_text = seed_text

    for _ in range(length):
        # Pad the sequence to the required length
        input_seq_padded = np.pad(input_seq, (SEQ_LENGTH - len(input_seq), 0), mode='constant')[-SEQ_LENGTH:]
        input_seq_padded = np.expand_dims(input_seq_padded, axis=0)

        # Predict the next character
        predictions = model.predict(input_seq_padded, verbose=0)
        next_char_idx = np.argmax(predictions)
        next_char = idx_to_char[next_char_idx]

        # Append the character to the text
        generated_text += next_char
        input_seq.append(next_char_idx)

    return generated_text
"""
    )

def sourceSeq2seq():
    print(
"""
# Seq2Seq

def seq2seq(path):

    # Read the dataset file
    data_file = path  # Example file: English-Marathi
    pairs = []

    # Load data and preprocess
    with open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                pairs.append((parts[0].strip().lower(), parts[1].strip().lower()))

    df = pd.DataFrame(pairs, columns=["source", "target"])
    print("Sample Data:\n", df.head())
    
    # Add start and end tokens to target language
    df['target'] = df['target'].apply(lambda x: f"<start> {x} <end>")

    # Tokenization
    source_tokenizer = Tokenizer(filters='')
    target_tokenizer = Tokenizer(filters='')

    source_tokenizer.fit_on_texts(df['source'])
    target_tokenizer.fit_on_texts(df['target'])

    source_sequences = source_tokenizer.texts_to_sequences(df['source'])
    target_sequences = target_tokenizer.texts_to_sequences(df['target'])

    source_vocab_size = len(source_tokenizer.word_index) + 1
    target_vocab_size = len(target_tokenizer.word_index) + 1
    
    # Pad sequences
    max_source_len = max(len(seq) for seq in source_sequences)
    max_target_len = max(len(seq) for seq in target_sequences)

    source_sequences = pad_sequences(source_sequences, maxlen=max_source_len, padding='post')
    target_sequences = pad_sequences(target_sequences, maxlen=max_target_len, padding='post')

    # Split data into training and validation
    train_size = int(0.8 * len(source_sequences))
    X_train, X_val = source_sequences[:train_size], source_sequences[train_size:]
    y_train, y_val = target_sequences[:train_size], target_sequences[train_size:]

    # Model parameters
    embedding_dim = 256
    units = 512
    
    # Encoder
    class Encoder(tf.keras.Model):
        def __init__(self, vocab_size, embedding_dim, enc_units):
            super(Encoder, self).__init__()
            self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
            self.lstm = tf.keras.layers.LSTM(enc_units, return_sequences=True, return_state=True)

        def call(self, x):
            x = self.embedding(x)
            output, state_h, state_c = self.lstm(x)
            return output, state_h, state_c

    # Decoder
    class Decoder(tf.keras.Model):
        def __init__(self, vocab_size, embedding_dim, dec_units):
            super(Decoder, self).__init__()
            self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
            self.lstm = tf.keras.layers.LSTM(dec_units, return_sequences=True, return_state=True)
            self.fc = tf.keras.layers.Dense(vocab_size, activation='softmax')

        def call(self, x, enc_output, states):
            x = self.embedding(x)
            output, state_h, state_c = self.lstm(x, initial_state=states)
            x = self.fc(output)
            return x, state_h, state_c

    # Create encoder and decoder
    encoder = Encoder(source_vocab_size, embedding_dim, units)
    decoder = Decoder(target_vocab_size, embedding_dim, units)

    # Optimizer and loss
    optimizer = tf.keras.optimizers.Adam()
    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False, reduction='none')

    def loss_function(real, pred):
        mask = tf.math.logical_not(tf.math.equal(real, 0))
        loss = loss_object(real, pred)
        mask = tf.cast(mask, dtype=loss.dtype)
        loss *= mask
        return tf.reduce_mean(loss)

    # Training step
    @tf.function
    def train_step(source, target_in, target_out):
        loss = 0
        with tf.GradientTape() as tape:
            enc_output, enc_h, enc_c = encoder(source)
            dec_h, dec_c = enc_h, enc_c
            dec_input = target_in[:, 0:1]  # Start with the <start> token

            for t in range(1, target_out.shape[1]):
                predictions, dec_h, dec_c = decoder(dec_input, enc_output, [dec_h, dec_c])
                loss += loss_function(target_out[:, t], predictions)
                dec_input = tf.expand_dims(target_out[:, t], 1)

        batch_loss = loss / int(target_out.shape[1])
        variables = encoder.trainable_variables + decoder.trainable_variables
        gradients = tape.gradient(loss, variables)
        optimizer.apply_gradients(zip(gradients, variables))
        return batch_loss

    # Prepare data for training
    BATCH_SIZE = 64
    BUFFER_SIZE = len(X_train)
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
    val_dataset = tf.data.Dataset.from_tensor_slices((X_val, y_val)).batch(BATCH_SIZE)

    # Training loop
    EPOCHS = 10
    for epoch in range(EPOCHS):
        total_loss = 0
        for (batch, (source, target)) in enumerate(train_dataset):
            target_in = target[:, :-1]
            target_out = target[:, 1:]
            batch_loss = train_step(source, target_in, target_out)
            total_loss += batch_loss

        print(f"Epoch {epoch + 1}, Loss: {total_loss / batch}")

    return None
"""
    )
    return None

def sourceImports():

    print(
"""
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
install('tensorflow')

import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

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
"""
    )
    return None

