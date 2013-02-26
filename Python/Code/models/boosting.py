#! /usr/bin/env python

import sys, math, numpy, random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn import cross_validation

from lib import util, config

class BoostingSVM(object):
    """Boosting - using different (sample weighted) Support Vector Machines as underlying models"""
    def __init__(self, n_models):
        self.n_models   = n_models
        self.clf        = list()
        self.w          = None
        self.alpha      = numpy.matrix(numpy.zeros((self.n_models, 1)))
        self.eps        = numpy.matrix(numpy.zeros((self.n_models, 1)))
    def get_classifier(self):
        return SVC(C = 1, kernel = 'linear', class_weight = 'auto')
    def fit(self, x, y):
        """fit the training data to all the classifiers"""
        n_samples, n_features = x.get_shape()
        self.w = (1.0 / n_samples) * numpy.matrix(numpy.ones(n_samples))
        for i in xrange(0, self.n_models):
            clf = self.get_classifier()
            clf.fit(x, y, sample_weight = numpy.array(self.w[-1, :])[0])
            I = numpy.matrix(map(lambda f: int(f), clf.predict(x) != y))
            self.eps[i] = (self.w[-1, :] * I.transpose()) / self.w[-1, :].sum(1)
            if self.eps[i] == 0:
                self.alpha[i] = 1
            else:
                self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.vstack((self.w, (numpy.multiply(self.w[-1, :], numpy.exp(self.alpha[i] * I)))))
            self.clf.append(clf)
    def score(self, x, y):
        """return the accuracy of prediction on testing data"""
        predictions = None
        for i in xrange(0, self.n_models):
            if predictions is None:
                predictions = self.clf[i].predict(x)
            else:
                predictions = numpy.vstack((predictions, self.clf[i].predict(x)))
        predictions = numpy.sign(predictions.transpose() * self.alpha)
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
        clf = BoostingSVM(n_models)
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
        sys.exit(1)
