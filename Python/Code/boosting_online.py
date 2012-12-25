#! /usr/bin/env python

import sys
import math
import numpy
import scipy

from lib.util import get_comments_data
from lib.online_svm import OnlineSVM

class OnlineBoosting(object):

    def __init__(self, n_models):
        self.n_models   = n_models
        self.clf        = list()
        self.w          = list()
        self.alpha      = numpy.matrix(numpy.zeros((self.n_models, 1)))
        self.eps        = numpy.matrix(numpy.zeros((self.n_models, 1)))

    def get_classifier(self):
        return OnlineSVM(randomize = False)

    def predict(self, comment):
        '''return the prediction from the current set of models'''
        predictions = numpy.matrix(numpy.ones((self.n_models, 1)))
        for i in xrange(0, self.n_models):
            predictions[i] = self.clf[i].predict(comment)
        return numpy.sign(predictions.transpose() * self.alpha)

    def fit(self, comments, labels):
        '''fit all the models to the first two samples'''
        self.w = 0.5 * numpy.matrix(numpy.ones(2))
        for i in xrange(0, self.n_models):
            clf = self.get_classifier()
            clf.fit(comments, labels, sample_weight = numpy.array(self.w)[0])
            predictions = numpy.zeros((2, 1))
            for j in xrange(0, 2):
                predictions[j] = clf.predict(comments[j])
            I = numpy.matrix(map(lambda f: int(f), (predictions.transpose() != labels)[0]))
            self.eps[i] = (self.w * I.transpose()) / self.w.sum(1)
            if self.eps[i] == 0:
                self.alpha[i] = 1
            else:
                self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.multiply(self.w, scipy.exp(self.alpha[i] * I))
            self.clf.append(clf)

    def add(self, comment, label):
        '''update all the models with the current sample, and update the self.alpha values'''
        n_samples = float('inf')
        for i in xrange(0, self.n_models):
            self.clf[i].add(comment, label)
            if len(self.clf[i].support_vectors) < n_samples:
                n_samples = len(self.clf[i].support_vectors)
        self.w = (1.0 / n_samples) * numpy.matrix(numpy.ones(n_samples))
        for i in xrange(0, self.n_models):
            labels, comments = list(), list()
            for j in self.clf[i].support_vectors:
                labels.append(j[0])
                comments.append(j[1])
            predictions = numpy.zeros((len(labels), 1))
            for j in xrange(0, len(labels)):
                predictions[j] = self.clf[i].predict(comments[j])
            I = numpy.matrix(map(lambda f: int(f), (predictions.transpose() != labels)[0]))
            self.eps[i] = (self.w * I.transpose()) / self.w.sum(1)
            if self.eps[i] == 0:
                self.alpha[i] = 1
            else:
                self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.multiply(self.w, scipy.exp(self.alpha[i] * I))

def main(filename):
    # initial setup
    labels, _, comments = get_comments_data(filename)
    clf = OnlineBoosting(n_models = 5)

    # input first two samples (having different labels), and then continue with the online mode
    positive, negative = labels.index(1), labels.index(-1)
    clf.fit( [comments[positive], comments[negative]], [labels[positive], labels[negative]] )
    indices = [i for i in xrange(0, len(labels)) if i not in [positive, negative]]
    for i in indices:
        prediction = clf.predict(comments[i])
        clf.add(comments[i], labels[i])
        print "#%d \t (label, predicted) = (%d, %d)" % (i, labels[i], prediction)

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        print "Usage: python %s <training_file>" % sys.argv[0]
    else:
        main(filename)

