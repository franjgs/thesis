#! /usr/bin/env python

import sys, numpy

from lib import util, config
from lib.online_text_svm import OnlineTextSVM

class OnlineBagging(object):

    def __init__(self, n_models):
        self.n_models = n_models
        self.clf = list()

    def get_classifier(self):
        return OnlineTextSVM(randomize = True, factor = 0.5)

    def predict(self, story):
        '''return the prediction from the current set of models'''
        predictions = list()
        for i in xrange(0, self.n_models):
            predictions.append(self.clf[i].predict(story))
        return numpy.sign(sum(predictions))

    def fit(self, stories, labels):
        '''fit all the models to the first few samples'''
        for i in xrange(0, self.n_models):
            self.clf.append(self.get_classifier())
            self.clf[i].fit(stories, labels)

    def add(self, story, label):
        '''update all the models with the current sample'''
        for i in xrange(0, self.n_models):
            self.clf[i].add(story, label)

def main():
    # initial setup
    labels, stories = util.get_distress_data(config.CONNECTION)
    clf = OnlineBagging(n_models = 5)
    total, correct = 0.0, 0.0

    # input first two samples (having different labels), and then continue with the online mode
    positive, negative = labels.index(1), labels.index(-1)
    clf.fit( [stories[positive], stories[negative]], [labels[positive], labels[negative]] )
    indices = [i for i in xrange(0, len(labels)) if i not in [positive, negative]]
    for i in indices:
        prediction = clf.predict(stories[i])
        clf.add(stories[i], labels[i])
        if prediction == labels[i]:
            correct = correct + 1
        total = total + 1
        print "#%d => Cumulative accuracy = %.3f" % (i, correct / total)

if __name__ == "__main__":
    main()

