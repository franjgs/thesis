#! /usr/bin/env python

import sys, numpy, random
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation

from lib import util, config

class BaggingSVM(object):
    """
    Bagging -
        Uses Support Vector Machines as underlying models
        Each model is trained with a different and random subset of samples
    """
    def __init__(self, n_models):
        self.n_models = n_models
        self.clf = list()
    def get_classifier(self):
        return LinearSVC(C = 1, class_weight = 'auto')
    def fit(self, x, y):
        """fit the training data to all the classifiers"""
        n_samples = x.get_shape()[0]
        for i in xrange(0, self.n_models):
            self.clf.append(self.get_classifier())
            indices = random.sample(xrange(0, n_samples), random.randrange(n_samples / 2, n_samples))
            self.clf[i].fit(x[indices, :], y[indices, :])
    def score(self, x, y):
        """return the accuracy of prediction on testing data"""
        predictions = None
        for i in xrange(0, self.n_models):
            if predictions is None:
                predictions = self.clf[i].predict(x)
            else:
                predictions = numpy.vstack((predictions, self.clf[i].predict(x)))
        predictions = numpy.sign(predictions.transpose().sum(1))
        return numpy.mean(predictions == y)

def main(filename):
    # initialize global data
    labels, _, comments = util.get_comments_data(filename)
    vec = TfidfVectorizer(
        ngram_range = (1, 2),
        strip_accents = None,
        charset_error = 'ignore',
        stop_words = None,
        min_df = 2
    )
    labels, instances = numpy.array(labels), vec.fit_transform(comments)
    random.seed(0)
    
    # cross validate
    n_models = 9; cv = 5; cv_accuracy = list();
    for i in xrange(0, cv):
        print "Iteration #" + str(i) + "..."
        
        # initialize training/testing data
        cv_data = cross_validation.train_test_split(instances, labels, test_size = 0.3, random_state = i)
        x_training = cv_data[0]
        x_testing = cv_data[1]
        y_training = cv_data[2]
        y_testing = cv_data[3]
        
        # initialize the classifier
        clf = BaggingSVM(n_models)
        clf.fit(x_training, y_training)
        
        # measure prediction accuracy
        cv_accuracy.append(clf.score(x_testing, y_testing))
    
    print "Scores => " + str(cv_accuracy)
    print "Mean   => " + str(numpy.mean(cv_accuracy))

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except Exception, e:
        print "Usage: python %s <filename>" % sys.argv[0]
        raise e
