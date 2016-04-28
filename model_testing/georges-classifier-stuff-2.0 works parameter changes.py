from sklearn import svm

from dataset import load_data

from sklearn import cross_validation

from sklearn import datasets

from sklearn.cross_validation import train_test_split

from sklearn.grid_search import GridSearchCV

from sklearn.metrics import classification_report

import matplotlib.pyplot as plt

import numpy as np
from sklearn.utils import shuffle

#This is where your clf will be (model)

scores, targets, acc = load_data()

'''

# Loading the Digits dataset

digits = datasets.load_digits()



# To apply an classifier on this data, we need to flatten the image, to

# turn the data in a (samples, feature) matrix:

n_samples = len(digits.images)

scores = digits.images.reshape((n_samples, -1))

targets = digits.target

'''

# Split the dataset in two equal parts

X_train, X_test, y_train, y_test = train_test_split(

    scores, targets, test_size=0.5, random_state=0)



# Set the parameters by cross-validation

tuned_parameters = [{'C':[  3.12500000e-02,   7.06322365e-02,   1.59645210e-01,
         3.60835144e-01,   8.15570983e-01,   1.84337928e+00,
         4.16646404e+00,   9.41717355e+00,   2.12849929e+01,
         4.81090129e+01,   1.08737510e+02,   2.45771952e+02,
         5.55501524e+02,   1.25556208e+03,   2.83786105e+03,
         6.41422312e+03,   1.44976296e+04,   3.27680000e+04]
,'cache_size':[200],'class_weight':['balanced'], 'coef0':[0.0],
'decision_function_shape':[None],'degree':[1,2,3,4,5,6],'gamma':[  3.05175781e-05,   6.35751960e-05,   1.32441884e-04,
         2.75907174e-04,   5.74778659e-04,   1.19739731e-03,
         2.49445641e-03,   5.19653148e-03,   1.08255808e-02,
         2.25521965e-02,   4.69814579e-02,   9.78732776e-02,
         2.03892746e-01,   4.24755897e-01,   8.84865086e-01,
         1.84337928e+00,   3.84018675e+00,   8.00000000e+00]
,'kernel':['rbf','poly','linear','sigmoid'],'max_iter':[-1]

}]
'''
,'probability':['False'], 'random_state':[None], 'shrinking':['True','False'],
  'tol':[1e-3], 'verbose':[1]
{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],

                     'C': [1, 10, 100, 1000]},

                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
                    '''



scores2 = ['precision', 'recall']

'''

clf = svm.SVC(

C=1.0, cache_size=200, class_weight=None, coef0=0.0,

  decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',

  max_iter=-1, probability=False, random_state=None, shrinking=True,

  tol=0.001, verbose=False

)



clf.fit(scores,targets)

scores = cross_validation.cross_val_score(clf, scores, targets, cv=10, scoring='accuracy')

'''

for score in scores2:



    print("# Tuning hyper-parameters for %s" % score)

    print()



    clf = GridSearchCV(svm.SVC(C=1), tuned_parameters, cv=5,

                       scoring='%s_weighted' % score)
    clf.fit(X_train, y_train)



    print("Best parameters set found on development set:")

    print()

    print(clf.best_params_)

    print()

    print("Grid scores on development set:")

    print()

    print('Mean Score...StD\tHyperparameters')

    for params, mean_score, grid_scores in clf.grid_scores_:
        pass
     #   print("%0.3f (+/-%0.03f) for %r" % (mean_score, grid_scores.std() * 2, params))

    print()



    print("Detailed classification report:")

    print()

    print("The model is trained on the full development set.")

    print("The scores are computed on the full evaluation set.")

    print()

    y_true, y_pred = y_test, clf.predict(X_test)

    print(classification_report(y_true, y_pred))

    print()



# Note the problem is too easy: the hyperparameter plateau is too flat and the

# output model is the same for precision and recall with ties in quality.









