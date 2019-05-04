import src.extractAllTestWords
import src.calcWordStats
import src.commonWordFilter
import src.accountForMisspell
import src.applyDelWordStatAndCount
import src.extractAllTestWordsSingQuote
import src.calcWordStatsSingQuote
import src.commonWordFilterSingleQuote

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
                               args.workDir+'/testWordCounts.csv')
   src.calcWordStats.run(args.train,
                     args.workDir+'/trainWordStats.csv')
   # Check spelling on trainign set
   src.accountForMisspell.run(args.workDir+'/trainWordStats.csv',\
                              args.workDir+'/trainMisspell.csv')
   # Remove all training words not recognized
   src.applyDelWordStatAndCount.run(
           args.workDir+'/trainMisspell.csv',
           args.workDir+'/testWordCounts.csv',
           args.workDir+'/trainWordStats.csv',
           args.workDir+'/testWordCountsDel.csv',
           args.workDir+'/trainWordStatsDel.csv'
           )
   # Remove all words not common in both sets
   src.commonWordFilter.run(args.workDir+'/testWordCountsDel.csv',
                            args.workDir+'/trainWordStatsDel.csv',
                            args.workDir+'/testWordCountsFilterDel.csv',
                            args.workDir+'/trainWordStatsFilterDel.csv' )
   # Expand this set if single quote was asked for
   if args.singQuote:
          src.extractAllTestWords.run(
                  args.test,
                  args.workDir+'/testWordCountsSingQuote.csv')
          src.calcWordStats.run(
                  args.train,
                  args.workDir+'/trainWordStatsSingQuote.csv')
          src.accountForMisspell.run(
                  args.workDir+'/trainWordStatsSingQuote.csv',\
                  args.workDir+'/trainMisspellSingQuote.csv')
          src.applyDelWordStatAndCount.run(
                  args.workDir+'/trainMisspellSingQuote.csv',
                  args.workDir+'/testWordCountsSingQuote.csv',
                  args.workDir+'/trainWordStatsSingQuote.csv',
                  args.workDir+'/testWordCountsDelSingQuote.csv',
                  args.workDir+'/trainWordStatsDelSingQuote.csv'
                  )
          src.commonWordFilter.run(
                  args.workDir+'/testWordCountsDelSingQuote.csv',
                  args.workDir+'/trainWordStatsDelSingQuote.csv',
                  args.workDir+'/testWordCountsFilterDelSingQuoteHold.csv',
                  args.workDir+'/trainWordStatsFilterDelSingQuoteHold.csv' 
                  )
          catCmd = 'cat '+args.workDir+'/testWordCountsFilterDel.csv'\
              ' '+args.workDir+'/testWordCountsFilterDelSingQuoteHold.csv'\
              ' > '+args.workDir+'/testWordCountsFilterDelSingQuote.csv'
          os.system(catCmd)
          catCmd = 'cat '+args.workDir+'/trainWordStatsFilterDel.csv'\
              ' '+args.workDir+'/trainWordStatsFilterDelSingQuoteHold.csv'\
              ' > '+args.workDir+'/testWordCountsFilterDelSingQuote.csv'
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

    parser.add_argument('-wd','--workDir',required=False,
        default=os.path.dirname(os.path.realpath(__file__))+\
        '../data',help='A directory that will store files intermediate files '\
        +'generated')

    args = parser.parse_args()
    
    main(args)
