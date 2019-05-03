import re

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import WordPunctTokenizer
from keras.preprocessing import text, sequence
from keras.utils import np_utils
from keras import backend as K
from bs4 import BeautifulSoup


MAX_WORDS = 10000
MAX_LEN = 30


def clean_text(text):
    """
    A function to pre-process text

    Parameters
    ----------
    text : string
        the string to be processed
    Returns
    -------
    text : string
        a clean string
    """
    tok = WordPunctTokenizer()
    pat1 = r'@[A-Za-z0-9]+'
    pat2 = r'https?://[A-Za-z0-9./]+'
    combined_pat = r'|'.join((pat1, pat2))
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    letters_only = re.sub("[^a-zA-Z]", " ", clean)
    lower_case = letters_only.lower()
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip()


def precision(y_true, y_pred):
    """Precision metric.
    Only computes a batch-wise average of precision.
    Computes the precision, a metric for multi-label classification of
    how many selected items are relevant.

    Parameters
    ----------
    y_true : numpy array
        an array of true labels
    y_pred : numpy array
        an array of predicted labels

    Returns
    -------
    recall : float
        the batch-wise average of precision value
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def recall(y_true, y_pred):
    """Recall metric.
    Only computes a batch-wise average of recall.
    Computes the recall, a metric for multi-label classification of
    how many relevant items are selected.

    Parameters
    ----------
    y_true : numpy array
        an array of true labels
    y_pred : numpy array
        an array of predicted labels

    Returns
    -------
    recall : float
        the batch-wise average of recall value
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def fbeta_score(y_true, y_pred, beta=1):
    """Computes the F score.
    The F score is the weighted harmonic mean of precision and recall.
    Here it is only computed as a batch-wise average, not globally.
    This is useful for multi-label classification, where input samples can be
    classified as sets of labels. By only using accuracy (precision) a model
    would achieve a perfect score by simply assigning every class to every
    input. In order to avoid this, a metric should penalize incorrect class
    assignments as well (recall). The F-beta score (ranged from 0.0 to 1.0)
    computes this, as a weighted mean of the proportion of correct class
    assignments vs. the proportion of incorrect class assignments.
    With beta = 1, this is equivalent to a F-measure. With beta < 1, assigning
    correct classes becomes more important, and with beta > 1 the metric is
    instead weighted towards penalizing incorrect class assignments.

    Parameters
    ----------
    y_true : numpy array
        an array of true labels
    y_pred : numpy array
        an array of predicted labels
    beta : float
        ranged from 0 to 1 used as a weight to compute the weighted mean of
        the precision and recall.
    Returns
    -------
    recall : float
        the batch-wise average of fbeta score
    """
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')

    # If there are no true positives, fix the F score at 0 like sklearn.
    if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
        return 0

    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    bb = beta ** 2
    fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
    return fbeta_score


def fmeasure(y_true, y_pred):
    """Computes the f-measure, the harmonic mean of precision and recall.
    Here it is only computed as a batch-wise average, not globally.

    Parameters
    ----------
    y_true : numpy array
        an array of true labels
    y_pred : numpy array
        an array of predicted labels

    Returns
    -------
    recall : float
        the batch-wise average of fmeasure value
    """
    return fbeta_score(y_true, y_pred, beta=1)


def data_loader(training_file, test_file, text_clmn='comment_text',
                target_clmn='target', preprocess=True):
    """ A function to read the training and test files and convert them
    into arrays readable by the deep neural network.

    Parameters
    ----------
    training_file : string
        the path to the training file
    test_file : string
        the path to the test file
    text_clmn : string
        a string that specifies the name of the text column
    target_clmn : string
        a string that specifies the name of the label column
    preprocess : bool
        if True, the text will be preprocessed and cleaned

    Returns
    -------
    X_train_seq : numpy matrix
        a matrix of float numbers representing the training set text
    t_train : numpy array
        a one-hot encoding input labels
    X_test_seq : numpy matrix
        a matrix of float numbers representing the test set text
    """

    train_df = pd.read_csv(training_file)
    test_df = pd.read_csv(test_file)

    train_df[target_clmn] = train_df[target_clmn].apply(lambda x: 0 if x < 0.5 else 1)

    if preprocess:
        train_df[text_clmn] = train_df[text_clmn].apply(lambda x: clean_text(x))
        test_df[text_clmn] = test_df[text_clmn].apply(lambda x: clean_text(x))

    # Convert labels to one-hot encoding
    y_train = train_df[target_clmn]
    encoder = LabelEncoder()
    encoder.fit(y_train)
    encoder = encoder.transform(y_train)
    y_train = np_utils.to_categorical(encoder)

    X_train_text = train_df[text_clmn]
    X_test_text = test_df[text_clmn]
    all_text = X_train_text.append(X_test_text)

    # convert text to sequence
    tokenizer = text.Tokenizer(num_words=MAX_WORDS)
    tokenizer.fit(all_text)

    X_train_seq = tokenizer.texts_to_sequences(X_train_text)
    X_train_seq = sequence.pad_sequences(X_train_seq, maxlen=MAX_LEN)

    X_test_seq = tokenizer.texts_to_sequences(X_test_text)
    X_test_seq = sequence.pad_sequences(X_test_seq, maxlen=MAX_LEN)

    return X_train_seq, y_train, X_test_seq, tokenizer


def build_embeddings(embed_file, word_index):
    """ A function to read the embedding file and create an embedding
    matrix for input text.

    Parameters
    ----------
    embed_file : string
        the path to the embedding file
    word_index : np array
        an array that keeps the index of the words

    Returns
    -------
    embeddin_matrix : numpy matrix
        a matrix of float numbers representing all words
    """
    embeddings_index = {}
    for line in open(embed_file):
        values = line.split()
        embeddings_index[values[0]] = np.asarray(values[1:], dtype='float32')

    embedding_matrix = np.zeros((len(self.word_index) + 1, 300))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return embedding_matrix
