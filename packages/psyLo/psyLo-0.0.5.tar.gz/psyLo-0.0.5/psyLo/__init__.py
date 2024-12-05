# to allow users to do things like - from psyLo import testLib
from .main import testLib


# nlp
from .nlp import (
    rmExcessWhitespaces,
    rmHTML,
    rmURL,
    rmSpecialChar,
    rmPunctuation,
    rmNumbers,
    tokenize,
    rmStopWords,
    wordNetLemmatize,
    porterStemmer,
    help,
    example
)

# Deep Learning

from .dl import (
    ann,
    cnn,
    rnn,
    transLearn,
    lstm,
    help
)