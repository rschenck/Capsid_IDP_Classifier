#!/usr/bin/env python

import sys
import operator
import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from scipy import interp
from datasets import load_data

# obtains the classifications from the final curated dataset
def get_targets():
	with open('/Users/schencro/Desktop/FINAL_DATASET/Curated_Dataset/FINAL_CURATED_TABLE.csv','r') as table:
		typed = {}
		for line in table:
			line = line.split(',')
			acc = line[1].rstrip(' ')
			typed.update({acc:line[2]})
	return typed

# obtain FINAL_DATASET for model (all data)
def get_data():
	with open('/Users/schencro/Desktop/FINAL_DATASET/Curated_Dataset/FINAL_CURATED_SCORES.csv', 'r') as scores:
		scores = scores.readlines()
	formatted = []
	for item in scores:
		item = item.rstrip('\n')
		item = item.split(',')
		sample = [item[0]]
		for i in range(1, len(item)):
			 ind = float(item[i])
			 sample.append(ind)
		formatted.append(sample)
	scores = None
	return formatted

# get arrays after fetching the proper classification and getting that classifications set of scores
def get_arrays(types, scores):
	order_types = []
	out_scores = []
	for item in scores:
		acc = item[0]
		ctype = types[acc]
		order_types.append(ctype)
		del item[0]
		out_scores.append(item)

	# the arrays needed for cross validation
	type_array = np.asarray(order_types)
	scores = np.asarray(out_scores)

	# cleanup
	item = None
	ourder_types = None
	out_scores = None

	return scores, type_array

# ExtraTreesClassifier model
def extratrees_model(x, y):
	clf = ExtraTreesClassifier(n_estimators=25, class_weight={"Type A":0.3,"Type B":0.5,"Neither":0.2}, bootstrap=False, max_features=125, criterion='gini', n_jobs=-1)
	clf = clf.fit(x, y)
	return clf

# Voting model
def results_vote(x, y):
	pass

# Section for running loops on different parameters
def tune_model_parameters(data, targets):
	# cross validate and tuning of the ExtraTreesClassifier parameters
	my_range = range(1,20)
	n_scores = []
	for n in my_range:
		clf = ExtraTreesClassifier(n_estimators=25, class_weight={"Type A":0.3,"Type B":0.5,"Neither":0.2}, bootstrap=False, max_features=125, criterion='gini', n_jobs=-1)
		scores = cross_validation.cross_val_score(clf, data, targets, cv=10, scoring='accuracy')
		n_scores.append(scores.mean())

	plt.plot(my_range,n_scores)
	plt.xlabel('Number of Trees in the Forest')
	plt.ylabel('Cross-Validated Accuracy (10-fold Mean)')
	plt.show()
	#plt.savefig('/Users/ryan/Desktop/FINAL_DATASET/Curated_Dataset/Capsid_Classifier/max_features_10_126.png', bbox_inches = 'tight')

	# get the parameter with the maximum mean output
	m = max(n_scores)
	mi = min(n_scores)
	print 'Max Accuracy: ' + repr(m)
	index = [i for i, j in enumerate(n_scores) if j == m]
	for i in index:
		print 'Parameter value max: ' + repr(my_range[i])
	indexmi = [i for i, j in enumerate(n_scores) if j == mi]
	print 'Min Accuracy: ' + repr(mi)
	for i in indexmi:
		print 'Parameter value min: ' + repr(my_range[i])

# get ROC curves for the predictions
def get_roc(data, targets):
	# binarize the classifactions
	bi_targets = label_binarize(targets, classes=['Type A', 'Type B', 'Neither'])
	#print bi_targets
	#print targets
	n_classes = bi_targets.shape[1]
	#print n_classes

	# shuffle and split training and test sets
	X_train, X_test, y_train, y_test = train_test_split(data, bi_targets, train_size=.8)

	# convert array to array of strings instead of arrays of arrays for the classifier (for the weights)
	string_test = []
	for i in range(0, len(y_train)):
		string_test.append(str(y_train[i]))
	string_test = np.asarray(string_test)

	clf = ExtraTreesClassifier(n_estimators=25, class_weight={"[1 0 0]":0.4,"[0 1 0]":0.5,"[0 1 0]":0.1}, bootstrap=False, max_features=125, criterion='gini', n_jobs = -1)
	model = clf.fit(X_train, string_test)

	y_score = model.predict(X_test)
	
	# get output of scores from string list into a np array
	array_scores = []
	for item in y_score:
		ind = item.split(' ')
		ind0 = ind[0].lstrip('[')
		ind1 = ind[1]
		ind2 = ind[2].rstrip(']')
		ind = [int(ind0),int(ind1), int(ind2)]
		array_scores.append(ind)
	array_scores = np.asarray(array_scores)
	print array_scores
	
	# Compute ROC curve and ROC area for each class
	fpr = dict()
	tpr = dict()
	roc_auc = dict()
	for i in range(n_classes):
		fpr[i], tpr[i], _ = roc_curve(y_test[:, i], array_scores[:, i])
		roc_auc[i] = auc(fpr[i], tpr[i])

	# Compute micro-average ROC curve and ROC area
	fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), array_scores.ravel())
	roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
	'''
	plt.figure()
	plt.plot(fpr[2], tpr[2], label='ROC curve (area = %0.2f)' % roc_auc[2])
	plt.plot([0, 1], [0, 1], 'k--')
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Receiver operating characteristic example')
	plt.legend(loc="lower right")
	plt.show()
	'''
	# Plot ROC curves for the multiclass problem

	# Compute macro-average ROC curve and ROC area

	# First aggregate all false positive rates
	all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

	# Then interpolate all ROC curves at this points
	mean_tpr = np.zeros_like(all_fpr)
	for i in range(n_classes):
	    mean_tpr += interp(all_fpr, fpr[i], tpr[i])

	# Finally average it and compute AUC
	mean_tpr /= n_classes

	fpr["macro"] = all_fpr
	tpr["macro"] = mean_tpr
	roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

	# Plot all ROC curves
	plt.figure()
	plt.plot(fpr["micro"], tpr["micro"],
	         label='micro-average ROC curve (area = {0:0.2f})'
	               ''.format(roc_auc["micro"]),
	         linewidth=2)

	plt.plot(fpr["macro"], tpr["macro"],
	         label='macro-average ROC curve (area = {0:0.2f})'
	               ''.format(roc_auc["macro"]),
	         linewidth=2)

	for i in range(n_classes):
	    plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.2f})'
	                                   ''.format(i, roc_auc[i]))

	plt.plot([0, 1], [0, 1], 'k--')
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Receiver operating characteristics')
	plt.legend(loc="lower right")
	plt.savefig('/Users/schencro/Desktop/FINAL_DATASET/Curated_Dataset/Capsid_Classifier/ROC_curves.eps', bbox_inches = 'tight')

# plot confusion matrices
def plot_confusion_matrix(cm, labels, title='Confusion matrix', cmap=plt.cm.Greens):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def cm_model_p1(X_train, y_train):
	clf = ExtraTreesClassifier(n_estimators=25, class_weight={"Type A":0.3,"Type B":0.5,"Neither":0.2}, bootstrap=False, max_features=125, criterion='gini', n_jobs=-1)
	model = clf.fit(X_train, y_train)
	return model

def cm_model_p2(model, X_test):
	# generate 100 predictions and vote for the majority for final prediction
	hundred_pred = []
	for i in range(0,100):
		y_pred = model.predict(X_test)
		hundred_pred.append(y_pred)
	final_pred = []
	for i in range(0, len(hundred_pred[0])):
		types = []
		for k,t in enumerate(hundred_pred):
			types.append(hundred_pred[k][i])
		counts = [types.count('Type A'),types.count('Type B'),types.count('Neither')]
		index, value = max(enumerate(counts), key=operator.itemgetter(1))
		if index == 0:
			final_pred.append('Type A')
		elif index == 1:
			final_pred.append('Type B')
		elif index == 2:
			final_pred.append('Neither')
		else:
			pass
	y_pred = np.asarray(final_pred)
	return y_pred

# Generate confusion matrix
def get_conf_matrix(data, targets):
	# shuffle and split training and test sets
	X_train, X_test, y_train, y_test = train_test_split(data, targets, train_size=.8)

	# gets the model for predictions
	model = cm_model_p1(X_train, y_train)
	
	# generate 100 confusion matrices, get mean value for each
	out_cm = np.zeros((3,3))
	for i in range(0,100):
		y_pred = cm_model_p2(model, X_test)
		# Compute confusion matrix
		labels = ['Type A', 'Type B', 'Neither']
		cm = confusion_matrix(y_test, y_pred, labels=labels)
		np.set_printoptions(precision=2)
		# Normalize the confusion matrix by row (i.e by the number of samples
		# in each class)
		cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
		out_cm += cm_normalized
	print out_cm
	cm_normalized = np.divide(out_cm, 100.0)

	print('Normalized confusion matrix (Mean of 100 predictions)')
	print(cm_normalized)
	plt.figure()
	plot_confusion_matrix(cm_normalized, labels, title='Normalized confusion matrix')
	# plt.show()
	plt.savefig('/Users/schencro/Desktop/FINAL_DATASET/Curated_Dataset/Capsid_Classifier/confusion_matrix_RYANFINAL_100mean.eps', bbox_inches = 'tight')
	
def main():
	'''
	# Use these three to get the data loaded, targets loaded, and the accessions stripped (Otherwise use dataset.py load_data())
	# get classifications
	type_dict = get_targets()

	# load data
	scores = get_data()
	
	# get arrays of scores and targets
	data, targets = get_arrays(type_dict, scores)
	'''

	data, targets = load_data()

	# tune model parameters
	#tune_model_parameters(data,targets)

	# get ROC curves
	#get_roc(data, targets)

	# get confusion matrix
	get_conf_matrix(data, targets)

	'''I WANT TO RE-RUN the ROC curves and the Confusion matrix data using predictions from a cross-validation rather than train/test_split'''


if __name__ == "__main__":
	main()