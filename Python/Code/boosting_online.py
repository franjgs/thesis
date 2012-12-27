#! /usr/bin/env python

import sys
import math
import numpy
import scipy

from lib import util, config
from lib.online_text_svm import OnlineTextSVM

class OnlineBoosting(object):

    def __init__(self, n_models):
        self.n_models   = n_models
        self.clf        = list()
        self.w          = list()
        self.alpha      = numpy.matrix(numpy.zeros((self.n_models, 1)))
        self.eps        = numpy.matrix(numpy.zeros((self.n_models, 1)))

    def get_classifier(self):
        return OnlineTextSVM(randomize = False)

    def predict(self, story):
        '''return the prediction from the current set of models'''
        predictions = numpy.matrix(numpy.ones((self.n_models, 1)))
        for i in xrange(0, self.n_models):
            predictions[i] = self.clf[i].predict(story)
        return numpy.sign(predictions.transpose() * self.alpha)

    def fit(self, stories, labels):
        '''fit all the models to the first two samples'''
        self.w = 0.5 * numpy.matrix(numpy.ones(2))
        for i in xrange(0, self.n_models):
            clf = self.get_classifier()
            clf.fit(stories, labels, sample_weight = numpy.array(self.w)[0])
            predictions = numpy.zeros((2, 1))
            for j in xrange(0, 2):
                predictions[j] = clf.predict(stories[j])
            I = numpy.matrix(map(lambda f: int(f), (predictions.transpose() != labels)[0]))
            self.eps[i] = (self.w * I.transpose()) / self.w.sum(1)
            if self.eps[i] == 0:
                self.alpha[i] = 1
            else:
                self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.multiply(self.w, scipy.exp(self.alpha[i] * I))
            self.clf.append(clf)

    def add(self, story, label):
        '''update all the models with the current sample, and update the self.alpha values'''
        n_samples = float('inf')
        for i in xrange(0, self.n_models):
            self.clf[i].add(story, label)
            if len(self.clf[i].support_vectors_x) < n_samples:
                n_samples = len(self.clf[i].support_vectors_x)
        self.w = (1.0 / n_samples) * numpy.matrix(numpy.ones(n_samples))
        for i in xrange(0, self.n_models):
            labels, stories = self.clf[i].support_vectors_y, self.clf[i].support_vectors_x
            predictions = numpy.zeros((len(labels), 1))
            for j in xrange(0, len(labels)):
                predictions[j] = self.clf[i].predict(stories[j])
            I = numpy.matrix(map(lambda f: int(f), (predictions.transpose() != labels)[0]))
            self.eps[i] = (self.w * I.transpose()) / self.w.sum(1)
            if self.eps[i] == 0:
                self.alpha[i] = 1
            else:
                self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.multiply(self.w, scipy.exp(self.alpha[i] * I))

def main():
    # initial setup
    labels, stories = util.get_distress_data(config.CONNECTION)
    clf = OnlineBoosting(n_models = 5)

    # input first two samples (having different labels), and then continue with the online mode
    positive, negative = labels.index(1), labels.index(-1)
    clf.fit( [stories[positive], stories[negative]], [labels[positive], labels[negative]] )
    indices = [i for i in xrange(0, len(labels)) if i not in [positive, negative]]
    for i in indices:
        prediction = clf.predict(stories[i])
        clf.add(stories[i], labels[i])
        print "#%d \t (label, predicted) = (%d, %d)" % (i, labels[i], prediction)

if __name__ == "__main__":
    main()

