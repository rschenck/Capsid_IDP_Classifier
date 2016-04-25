#!/usr/bin/env python
#Python Script developed by Ryan O. Schenck
#ryanschenck@mail.usf.edu
#University of South Florida


#Python v2.7.10
#Script constructed and ran on MacOSX 10.10.5

#numpy version 1.10.1
import numpy as np
#scikit learn version 0.16.1
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import metrics
#base
import sys

#user input to be tested
arg1 = sys.argv[1]


#ExtraTreesClassifier model set training
def extratrees_model(x, y):
	clf = ExtraTreesClassifier(n_estimators=1000, class_weight="auto", bootstrap=True)
	clf = clf.fit(x, y)

	return clf

#function to get the appropriate arrays for model building; returns scoresArray, typeArray, and nameArray
def get_arrays_training(filename):
	with open(filename, 'r') as dataset:
		#setup lists of both names and data
		nametemp = []
		scoretemp = []
		typetemp = []
		for line in dataset:
			#set up line to go into array
			line = line.rstrip('\n')
			line = line.split(',', 1)
			#takes the accession numbers and the scores
			accession = line[0]
			scores = line[1]

			#puts the accession into list for array
			nametemp.append(str(accession))

			#puts the scores into a list for array building
			singleScore = []
			scores = scores.split(',')
			for score in scores:
				#places each proteins score into an individual list
				singleScore.append(float(score))
			#creates a list of lists from the individual list
			scoretemp.append(singleScore)

		#places the names into one array
		nameArray = np.array(nametemp)
		#scores array and is what will be used for machine learning
		scoresArray = np.array(scoretemp)


	#get types into a dictionary
	with open('Rosario_etal_accession_numbers.txt', 'r') as getType:
		typedict = dict()
		for myLine in getType:
			myLine = myLine.rstrip('\n')
			myLine = myLine.split('\t')
			capType = myLine[1]
			name = myLine[0].replace(' ', '')
			typedict.update({name:capType})

	#builds list of types
	typetemp = []
	for val in nametemp:
		typetemp.append(typedict[val])

	#array containing types
	typeArray = np.array(typetemp)

	return scoresArray, typeArray, nameArray

def get_arrays_testing(filename):
	with open(filename, 'r') as dataset:
		#setup lists of both names and data
		nametemp = []
		scoretemp = []
		typetemp = []
		for line in dataset:
			#set up line to go into array
			line = line.rstrip('\n')
			line = line.split(',', 1)
			#takes the accession numbers and the scores
			accession = line[0]
			scores = line[1]

			#puts the accession into list for array
			nametemp.append(str(accession))

			#puts the scores into a list for array building
			singleScore = []
			scores = scores.split(',')
			for score in scores:
				#places each proteins score into an individual list
				singleScore.append(float(score))
			#creates a list of lists from the individual list
			scoretemp.append(singleScore)

		#places the names into one array
		nameArray = np.array(nametemp)
		#scores array and is what will be used for machine learning
		scoresArray = np.array(scoretemp)

	return scoresArray, nameArray



#get the arrays for training the model
trainScores, trainTypes, trainNames = get_arrays_training('train_dataset_80.txt')

#get the arrays for testing
testScores, testNames = get_arrays_testing(arg1)

#get the model to predict with
model = extratrees_model(trainScores, trainTypes)

#yields classifications of type and probability of each type
classification = model.predict(testScores)
proba = model.predict_proba(testScores)

with open('outFile.txt', 'w') as outFile:
	for index, value in enumerate(classification):
		print(testNames[index] + '\t' + value + '\t' + repr(proba[index]))
		outFile.write(testNames[index] + '\t' + value + '\t' + repr(proba[index]) + '\n')
