#! /usr/bin/env python

import math, numpy, scipy, sys, random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation
from sklearn.svm import LinearSVC

from lib import util, config

class StackingSVM(object):
    """Stacking - using different Support Vector Machines (trained on different features) as underlying models"""
    def __init__(self, n_models):
        self.n_models   = n_models
        self.models     = list()
        self.features   = list()
        self.clf        = None
    def get_classifier(self):
        return LinearSVC(C = 1, class_weight = 'auto')
    def fit(self, x, y):
        """fit the training data to all the classifiers"""
        # train all the first level classifiers on different features
        n_samples, n_features = x.get_shape()
        for i in xrange(0, self.n_models):
            model = self.get_classifier()
            features = random.sample(xrange(0, n_features), n_features / self.n_models)
            features.sort()
            model.fit(x[:, features], y)
            self.features.append(features)
            self.models.append(model)
        # transform the training dataset to second level
        training = None
        for i in xrange(0, self.n_models):
            if training is None:
                training = self.models[i].predict(x[:, self.features[i]])
            else:
                training = numpy.vstack((training, self.models[i].predict(x[:, self.features[i]])))
        training = training.transpose()
        # train the second level model
        self.clf = self.get_classifier()
        self.clf.fit(training, y)

    def score(self, x, y):
        """return the accuracy of prediction on testing data"""
        # convert the testing dataset to second level
        testing = None
        for i in xrange(0, self.n_models):
            if testing is None:
                testing = self.models[i].predict(x[:, self.features[i]])
            else:
                testing = numpy.vstack((testing, self.models[i].predict(x[:, self.features[i]])))
        testing = testing.transpose()
        # measure the predictions and return accuracy
        return numpy.mean(self.clf.predict(testing) == y)

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
        clf = StackingSVM(n_models)
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
