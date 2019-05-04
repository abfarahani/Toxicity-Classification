import src.calcWordSentiment
import src.calcSentimentStats

import os
import argparse

def main(args):
    src.calcWordSentiment.run(args.test, args.train, \
        args.workDir+"\testSentament.csv", args.workDir+"\trainSentament.csv",\
        args.singQuote, args.workDir)
    src.calcSentimentStats(args.workDir)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='These are the arguments '\
        + 'for formating Kaggle competition Jigsaw Unintended Bias in '\
        + 'Toxicity Classification data before applying sentament anylysis '\
        + 'to data')

    parser.add_argument('-train','--train',required=True,\
        help="Define the path to the training file provided by Kaggle.")

    parser.add_argument('-test','--test',required=True,\
        help="Define the path to the test file provided by the Kaggle "\
        +'competition')

    parser.add_argument('-wd','--workDir',required=False,\
        default=os.path.dirname(os.path.realpath(__file__))+"../data",\
        help="DPath to work directory used during the execution of previous "\
        + "steps in sentiment process")

    parser.add_argument('-singQuote','--singQuote',required=False,\
                        action='store_true',default=False, help="Use results "\
                        + "that included single quotes in words.")

    args = parser.parse_args()
    
    main(args)
    
