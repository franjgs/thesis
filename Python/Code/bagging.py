#! /usr/bin/env python

import random
random.seed(0)

from lib import util

import sys, numpy, scipy
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation

class BaggingSVM:
    def __init__(self, num_models):
        self.num_models = num_models
        self.models = list()
        self.features = list()
        for i in xrange(0, self.num_models):
            self.models.append(SVC(C = 1, kernel = 'linear', class_weight = 'auto'))
            self.features.append(None)
    def fit(self, x, y):
        n_samples, n_features = x.get_shape()
        for i in xrange(self.num_models):
            # pick random features for each classifier
            feature_indices = random.sample(xrange(0, n_features), n_features / self.num_models)
            feature_indices.sort()
            self.features[i] = feature_indices
            # train
            self.models[i].fit(x[:, feature_indices], y)
    def score(self, x, y):
        predictions = None
        for i in xrange(0, self.num_models):
            # build the data (with only the features assigned to this model)
            testing = x[:, self.features[i]]
            if predictions is None:
                predictions = self.models[i].predict(testing)
            else:
                predictions = scipy.vstack((predictions, self.models[i].predict(testing)))
        predictions = numpy.sign(predictions.transpose().sum(1))
        return numpy.mean(predictions == y)

def main(filename):
    # initialize global data
    vec = TfidfVectorizer(ngram_range = (1, 2))
    labels, _, comments = util.get_comments_data(filename)
    instances = vec.fit_transform(comments)

    # cross validate
    num_models = 5; cv = 5; cv_accuracy = list();
    for i in xrange(0, cv):
        print "Iteration #" + str(i) + "..."

        # initialize training/testing data
        cv_data = cross_validation.train_test_split(instances, labels, test_size = 0.5, random_state = i)
        x_training = cv_data[0]
        x_testing = cv_data[1]
        y_training = cv_data[2]
        y_testing = cv_data[3]

        # initialize the classifier
        clf = BaggingSVM(num_models)
        clf.fit(x_training, y_training)

        # measure prediction accuracy
        cv_accuracy.append(clf.score(x_testing, y_testing))

    print "Scores => " + str(cv_accuracy)
    print "Mean   => " + str(numpy.mean(cv_accuracy))

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print "Usage: python %s <training_file>" % sys.argv[0]

