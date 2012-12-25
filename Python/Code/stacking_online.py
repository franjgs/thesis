#! /usr/bin/env python

import sys
import math
import numpy
import scipy

from lib.util import get_comments_data
from lib.online_svm import OnlineSVM
from lib.online_text_svm import OnlineTextSVM

class OnlineStacking(object):

    def __init__(self, n_models):
        self.n_models = n_models
        self.models = list()
        self.clf = None

    def get_classifier(self, level):
        if level == 1:
            return OnlineTextSVM(randomize = False)
        elif level == 2:
            return OnlineSVM(randomize = False)

    def predict(self, comment):
        '''return the prediction from the current set of models'''
        # calculate the input for the second level classifier
        x = None
        for i in xrange(0, self.n_models):
            if x is None:
                x = self.models[i].predict(comment)
            else:
                x = scipy.vstack((x, self.models[i].predict(comment)))
        x = x.transpose()
        return self.clf.predict(x)

    def fit(self, comments, labels):
        '''fit all the models to the first two samples'''
        # train the first level models
        for i in xrange(0, self.n_models):
            self.models.append(self.get_classifier(level = 1))
            self.models[i].fit(comments, labels)
        # convert the data to second level training data
        x = None
        for i in xrange(0, self.n_models):
            if x is None:
                x = self.models[i].predict(comments)
            else:
                x = scipy.vstack((x, self.models[i].predict(comments)))
        x = x.transpose()
        # train the second level model
        self.clf = self.get_classifier(level = 2)
        self.clf.fit(x, labels)

    def add(self, comment, label):
        '''update all the models with the current sample'''
        for i in xrange(0, self.n_models):
            self.models[i].add(comment, label)
        x = None
        for i in xrange(0, self.n_models):
            if x is None:
                x = self.models[i].predict(comment)
            else:
                x = scipy.vstack((x, self.models[i].predict(comment)))
        x = x.transpose()
        self.clf.add(x, label)

def main(filename):
    # initial setup
    labels, _, comments = get_comments_data(filename)
    clf = OnlineStacking(n_models = 5)

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

