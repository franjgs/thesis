#! /usr/bin/env python

import random
random.seed(0)

from lib import util

import numpy
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation
from pprint import pprint

class SVM:
    def __init__(self):
        self.model = SVC(C = 1, kernel = 'linear', class_weight = 'auto')
    def fit(self, x, y):
        self.model.fit(x, y)
    def score(self, x, y):
        return numpy.mean(self.model.predict(x) == y)

# initialize the data
labels, _, comments = util.get_comments_data("Dataset/comments.csv")
vec = TfidfVectorizer(ngram_range = (1, 2), stop_words = 'english')
instances = vec.fit_transform(comments)

# cross validate
cv = 5; cv_accuracy = list();
for i in xrange(0, cv):
    print "Iteration #" + str(i) + "..."

    # initialize training/testing data
    cv_data = cross_validation.train_test_split(instances, labels, test_size = 0.5, random_state = i)
    x_training = cv_data[0]
    x_testing = cv_data[1]
    y_training = cv_data[2]
    y_testing = cv_data[3]

    # initialize the classifier
    clf = SVM()
    clf.fit(x_training, y_training)

    # measure prediction accuracy
    cv_accuracy.append(clf.score(x_testing, y_testing))

print "Scores => " + str(cv_accuracy)
print "Mean   => " + str(numpy.mean(cv_accuracy))

