#! /usr/bin/env python

import sys

from lib.util import get_comments_data
from lib.online_svm import OnlineSVM

class OnlineBagging(object):

    def __init__(self, n_models):
        self.n_models = n_models
        self.clf = list()

    def get_classifier(self):
        return OnlineSVM(randomize = True, factor = 0.5)

    def predict(self, comment):
        '''return the prediction from the current set of models'''
        predictions = list()
        for i in xrange(0, self.n_models):
            predictions.append(self.clf[i].predict(comment))
        return cmp(sum(predictions), 0)

    def fit(self, comments, labels):
        '''fit all the models to the first two samples'''
        for i in xrange(0, self.n_models):
            self.clf.append(self.get_classifier())
            self.clf[i].fit(comments, labels)

    def add(self, comment, label):
        '''update all the models with the current sample'''
        for i in xrange(0, self.n_models):
            self.clf[i].add(comment, label)

def main(filename):
    # initial setup
    labels, _, comments = get_comments_data(filename)
    clf = OnlineBagging(n_models = 5)

    # input first two samples (having different labels), and then continue with the online mode
    positive, negative = labels.index(1), labels.index(-1)
    clf.fit( [comments[positive], comments[negative]], [labels[positive], labels[negative]] )
    indices = [i for i in xrange(0, len(labels)) if i not in [positive, negative]]
    for i in indices:
        prediction = clf.predict(comments[i])
        clf.add(comments[i], labels[i])
        print "#%d \t (label, predicted) = (%d, %d)" % (i, prediction, labels[i])

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        print "Usage: python %s <training_file>" % sys.argv[0]
    else:
        main(filename)

