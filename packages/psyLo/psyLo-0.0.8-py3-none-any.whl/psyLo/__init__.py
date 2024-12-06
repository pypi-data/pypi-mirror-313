# to allow users to do things like - from psyLo import testLib
from .main import (
    testLib,
    printModules
)


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

    sentimentLogReg,
    sentimentRandomForest,

    textGeneration,
    seq2seq,

    help,
    example,

    sourceTextPreprocessing,
    sourceSentimentAnalysis,
    sourceTextGeneration,
    sourceSeq2seq
)

# Deep Learning

from .dl import (
    sourceANN,
    sourceCNN,
    sourceRNN,
    sourceLSTM,
    sourceTransLearn,
    help
)