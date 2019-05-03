import numpy as np
import pandas as pd

from sklearn import metrics
from keras import optimizers
from keras import regularizers
from keras.models import Sequential
from keras.models import Model
from keras.layers import LSTM
from keras.layers import Activation
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Bidirectional
from keras.layers import Input
from keras.layers import Embedding
from keras.layers import Conv1D
from keras.layers import MaxPooling1D
from keras.layers.merge import concatenate
from keras.callbacks import EarlyStopping
from keras.utils import plot_model


from util import fmeasure


class Model():
    def __init__(self, max_len=30, max_words=10000, batch_size=128,
                 loss='binary_crossentropy', optimizer='adam', n_epochs=10):
        self.max_len = max_len
        self.max_words = max_words
        self.batch_size = batch_size
        self.loss = loss
        self.optimizer = optimizer
        self.n_epochs = n_epochs
        self.model = Model()

    def build_lstm_model(self, word_index, emb_mat, d_rate=0.3):
        """ Builds an LSTM model

        Parameters
        ----------
        word_index : numpy array
            an array of index for all words
        emb_mat : numpy matrix
            a matrix of embedding values
        d_rate : float
            a float number indicating the dropout ratio.
        """
        lstm_input = layers.Input((70, ))
        lstm_layer = layers.Embedding(len(word_index) + 1, 300,
                                      weights=[emb_mat],
                                      trainable=False)(lstm_input)
        lstm_layer = layers.SpatialDropout1D(0.3)(lstm_layer)
        lstm_layer = SpatialDropout1D(d_rate)(lstm_layer)
        lstm_layer = Bidirectional(LSTM(128, return_sequences=True))(lstm_layer)
        lstm_layer = Bidirectional(LSTM(128, return_sequences=True))(lstm_layer)
        hidden = concatenate([
            GlobalMaxPooling1D()(lstm_layer),
            GlobalAveragePooling1D()(lstm_layer),
        ])
        hidden = add([hidden, Dense(512, activation='relu')(hidden)])
        hidden = add([hidden, Dense(512, activation='relu')(hidden)])
        lstm_output = Dense(1, activation='sigmoid')(hidden)

        self.model = Model(lstm_input, lstm_output)

    def build_cnn_model(self, word_index, emb_mat):
        """ Builds a CNN model

        Parameters
        ----------
        word_index : numpy array
            an array of index for all words
        emb_mat : numpy matrix
            a matrix of embedding values
        """
        cnn_input = layers.Input((70, ))
        emb_layer = layers.Embedding(len(word_index) + 1, 300,
                                     weights=[emb_mat],
                                     trainable=False)(cnn_input)
        emb_layer = layers.SpatialDropout1D(0.3)(emb_layer)
        conv_layer = layers.Convolution1D(100, 3, activation="relu")(emb_layer)
        pooling_layer = layers.GlobalMaxPool1D()(conv_layer)
        output_layer1 = layers.Dense(50, activation="relu")(pooling_layer)
        output_layer1 = layers.Dropout(0.25)(output_layer1)
        cnn_output = layers.Dense(1, activation="sigmoid")(output_layer1)
        self.model = Model(inputs=cnn_input, outputs=cnn_output)

    def train_model(self, X_train, y_train, class_weight={{0: 1.0, 1: 1.0}},
                    metrics=[fmeasure]):
        """ trains the model

        Parameters
        ----------
        X_train : numpy matrix
            a matrix of input text in the sequence format
        y_train : numpy array
            an array of input labels
        """
        self.model.compile(loss=self.loss, optimizer=optimizer)
        self.model.fit(X_train, y_train, class_weight=class_weight)

    def predict(self, X_test, test_df, submission_file):
        """ predicts labels for unseen data and stores them in a
        file for submission

        Parameters
        ----------
        X_test : numpy matrix
            a matrix of test text in the sequence format
        test_df : pandas dataframe
            the test test in the format of dataframe
        submission_file : string
            the path to the output dataframe ready to be submitted
        """
        predict = self.model.predict(X_test)
        test_df['prediction'] = predict
        test_df = test_df[['id', 'prediction']]
        test_df.to_csv(submission_file, index=False)

    def plot_model(self, outfile):
        """ plots the model

        Parameters
        ----------
        outfile : string
            the path to the output png file
        """
        plot_model(self.model, to_file=outfile, show_shapes=True)
