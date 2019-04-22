from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession

import os
import argparse

def randomForestClassifier(args):
    spark = SparkSession.builder.master("yarn") \
        .appName("randomForestClassifier") \
        .getOrCreate()
    #
    # Read in the data
    #

    print("Opening file: '" + args.train + "'")
    data = spark.read.format('libsvm').load(args.allData)
    trainingData = spark.read.format('libsvm').load(args.train)
    testingData = spark.read.format('libsvm').load(args.test)

    labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(data)

    # Treat all values as continuous (not categorical)
    featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=2).fit(data)

    (trainingData, testData) = data.randomSplit([0.7, 0.3])

    rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=10)

    labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                               labels=labelIndexer.labels)

    pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])

    model = pipeline.fit(trainingData)

    predictions = model.transform(testData)

    # Select example rows to display.
    predictions.select("predictedLabel", "label", "features").show(5)

    # Select (prediction, true label) and compute test error
    evaluator = MulticlassClassificationEvaluator(
        labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    print("Test Error = %g" % (1.0 - accuracy))

    rfModel = model.stages[2]
    print(rfModel)  # summary only

def main(args):
    #
    # Start by checking to ensure all command line arguments are valid
    #

    randomForestClassifier(args)

if __name__ == '__main__':
    #
    # Check for command line arguments
    #

    parser = argparse.ArgumentParser(description='This is part of the UGA CSCI 8360 Final Project. Please visit out GitHub project at https://github.com/dsp-uga/team-puzzle-final for more information regarding data organization, expectations, and examples of how to execute our scripts.')

    parser.add_argument('-train','--train',required=True,help='Training libsvm file')
    parser.add_argument('-test','--test',required=True,help='Testing libsvm file')
    parser.add_argument('-allData','--allData',required=True,help='Union of training and test data')

    args = parser.parse_args()

    main(args)
