import src.extractAllTestWords
import src.calcWordStats
import src.commonWordFilter
import src.accountForMisspell
import src.applyDelWordStatAndCount
import src.extractAllTestWordsSingleQuote
import src.calcWordStatsSingQuite
import src.commonWordFilterSingQuote

import os
import argparse

"""
This script takes the Kaggle train.csv and test.csv, reformats their content
in an intermediate directory, and ends with (depending on options selected)
files for later processing.
    

"""
def main(args):

   """
   Iterate through the formating steps
   """
   # Extract all words from files
   src.extractAllTestWords.run(args.test,
                               args.wordDir+'/testWordCounts.csv')
   src.calcWordStats.run(args.train,
                     args.wordDir+'/trainWordStats.csv')
   # Check spelling on trainign set
   src.accountForMisspell.run(args.wordDir+'/trainWordStats.csv',\
                              args.wordDir+'/trainMisspell.csv')
   # Remove all training words not recognized
   src.applyDelWordStatAndCount.run(
           args.wordDir+'/trainMisspell.csv',
           args.wordDir+'/testWordCounts.csv',
           args.wordDir+'/trainWordStats.csv',
           args.wordDir+'/testWordCountsDel.csv',
           args.wordDir+'/trainWordStatsDel.csv'
           )
   # Remove all words not common in both sets
   src.commonWordFilter.run(args.wordDir+'/testWordCountsDel.csv',
                            args.wordDir+'/trainWordStatsDel.csv',
                            args.wordDir+'/testWordCountsFilterDel.csv',
                            args.wordDir+'/trainWordStatsFilterDel.csv' )
   # Expand this set if single quote was asked for
   if args.singQuote:
          src.extractAllTestWords.run(
                  args.test,
                  args.wordDir+'/testWordCountsSingQuote.csv')
          src.calcWordStats.run(
                  args.train,
                  args.wordDir+'/trainWordStatsSingQuote.csv')
          src.accountForMisspell.run(
                  args.wordDir+'/trainWordStatsSingQuote.csv',\
                  args.wordDir+'/trainMisspellSingQuote.csv')
          src.applyDelWordStatAndCount.run(
                  args.wordDir+'/trainMisspellSingQuote.csv',
                  args.wordDir+'/testWordCountsSingQuote.csv',
                  args.wordDir+'/trainWordStatsSingQuote.csv',
                  args.wordDir+'/testWordCountsDelSingQuote.csv',
                  args.wordDir+'/trainWordStatsDelSingQuote.csv'
                  )
          src.commonWordFilter.run(
                  args.wordDir+'/testWordCountsDelSingQuote.csv',
                  args.wordDir+'/trainWordStatsDelSingQuote.csv',
                  args.wordDir+'/testWordCountsFilterDelSingQuoteHold.csv',
                  args.wordDir+'/trainWordStatsFilterDelSingQuoteHold.csv' 
                  )
          catCmd = 'cat '+args.wordDir+'/testWordCountsFilterDel.csv'\
              ' '+args.wordDir+'/testWordCountsFilterDelSingQuoteHold.csv'\
              ' > '+args.wordDir+'/testWordCountsFilterDelSingQuote.csv'
          os.system(catCmd)
          catCmd = 'cat '+args.wordDir+'/trainWordStatsFilterDel.csv'\
              ' '+args.wordDir+'/trainWordStatsFilterDelSingQuoteHold.csv'\
              ' > '+args.wordDir+'/testWordCountsFilterDelSingQuote.csv'
          os.system(catCmd)
    
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

    parser.add_argument('-singQuote','--singQuite',required=False,\
                        action='store_true',default=False)

    parser.add_argument('-wd','--wordDir',required=False,
        default=os.path.dirname(os.path.realpath(__file__))+\
        '../data',help='A directory that will store files intermediate files '\
        +'generated')

    args = parser.parse_args()
    
    main(args)
