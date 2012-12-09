#! /usr/bin/env python

from lib import util

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn import cross_validation
import math, numpy, scipy, random

class BoostingSVM:
    def __init__(self, num_models):
        self.num_models = num_models
        self.models     = list()
        self.w          = None
        self.alpha      = numpy.matrix(numpy.zeros((self.num_models, 1)))
        self.eps        = numpy.matrix(numpy.zeros((self.num_models, 1)))
    def fit(self, x, y, class_weight = None):
        n_samples, n_features = x.get_shape()
        self.w = (1.0 / n_samples) * numpy.matrix(numpy.ones(n_samples))
        for i in xrange(0, self.num_models):
            model = SVC(C = 1)
            model.fit(x, y, sample_weight = numpy.array(self.w)[0], class_weight = class_weight)
            I = numpy.matrix(map(lambda f: int(f), model.predict(x) != y))
            self.eps[i] = (self.w * I.transpose()) / self.w.sum(1)
            self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.multiply(self.w, scipy.exp(self.alpha[i] * I))
            self.models.append(model)
    def score(self, x, y):
        predictions = None
        for i in xrange(0, self.num_models):
            if predictions is None:
                predictions = self.models[i].predict(x)
            else:
                predictions = scipy.vstack((predictions, self.models[i].predict(x)))
        predictions = numpy.sign(predictions.transpose() * self.alpha)
        return numpy.mean(predictions == y)

# initialize global data
vec = TfidfVectorizer(ngram_range = (1, 2), stop_words = 'english')
labels, _, comments = util.get_comments_data("Dataset/comments.csv")
instances = vec.fit_transform(comments)

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
    clf = BoostingSVM(num_models)
    clf.fit(x_training, y_training)

    # measure prediction accuracy
    cv_accuracy.append(clf.score(x_testing, y_testing))

print "Scores => " + str(cv_accuracy)
print "Mean   => " + str(numpy.mean(cv_accuracy))

