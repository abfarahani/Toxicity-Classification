import argparse
import pandas as pd

from build_model import Model
from util import data_loader
from util import build_embeddings


def main():
    parser = argparse.ArgumentParser(description='reads input file and trains a model for toxicity classification')

    # Required arguments
    parser.add_argument("-i", "--input", required=True,
                        help="Path to training set")
    parser.add_argument("-t", "--test", required=True,
                        help="Path to test set")
    parser.add_argument("-o", "--output", required=True,
                        help="Path to submission file")
    parser.add_argument("-e", "--embedding", required=True,
                        help="Path to embedding file")
    
    # Optional arguments
    parser.add_argument("-c", "--text_column", type=str, default="commnet_text",
                        help="name of the column that contains the text")
    parser.add_argument("-l", "--label_column", type=str, default="target",
                        help="name of the column that contains the labels")
    parser.add_argument("-p", "--preprocess", type=bool, default=False,
                        help="if set the text will be processed before fed to the model")
    parser.add_argument("-m", "--model", type=str, choices=['LSTM','CNN'], default="LSTM",
                        help="the deep neural network")

    args = vars(parser.parse_args())

    # Loading the data
    X_train, y_train, X_test, tokenizer = data_loader(args['input'],
                                                      args['test'],
                                                      args['text_column'],
                                                      args['label_column'],
                                                      args['preprocess'])
    # Loading the embeddings
    word_index = tokenizer.word_index
    embedding_matrix = build_embeddings(args['embedding'], word_index)

    # building the model
    model_selection = args['model']
    Model = Model()
    if model_selection == 'LSTM':
        Model.buil_lstm()
    elif model_selection == 'CNN':
        Model.build_cnn()
    else:
        raise ValueError("the model must be CNN or LSTM")

    # Training the model
    Model.train(X_train, y_train)

    # Predicting the labels for test set
    test_df = pd.read_csv(args['test'])
    Model.predict(X_test, test_df, args['output'])
