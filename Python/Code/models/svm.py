#! /usr/bin/env python

import sys, numpy, random
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation

from lib import util, config

class SVM(object):
    """Simple wrapper on a Linear SVM (purely for consistency)"""
    def __init__(self):
        self.model = None
    def get_classifier(self):
        return LinearSVC(C = 1, class_weight = 'auto')
    def fit(self, x, y):
        if self.model is None:
            self.model = self.get_classifier()
        self.model.fit(x, y)
    def score(self, x, y):
        if self.model is None:
            return None
        return numpy.mean(self.model.predict(x) == y)

def main(filename):
    # initialize the data
    labels, timestamps, comments = util.get_comments_data(filename)
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
    cv = 5; cv_accuracy = list();
    for i in xrange(0, cv):
        print "Iteration #" + str(i) + "..."
        
        # initialize training/testing data
        cv_data = cross_validation.train_test_split(instances, labels, test_size = 0.3, random_state = i)
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

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except Exception, e:
        print "Usage: python %s <filename>" % sys.argv[0]
        sys.exit(1)
