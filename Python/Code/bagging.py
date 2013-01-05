#! /usr/bin/env python

import numpy, random
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation

from lib import util, config

class BaggingSVM(object):

    ''' Bagging - using different Support Vector Machines (each fed with different features) as underlying models '''

    def __init__(self, n_models, factor):
        self.n_models = n_models
        self.clf = list()
        self.features = list()
        self.factor = factor

    def get_classifier(self):
        return SVC(C = 1, kernel = 'linear', class_weight = 'auto')

    def fit(self, x, y):
        '''fit the training data to all the classifiers'''
        n_samples, n_features = x.get_shape()
        for i in xrange(0, self.n_models):
            self.clf.append(self.get_classifier())
            # pick random features for each classifier
            feature_indices = random.sample(xrange(0, n_features), int(n_features * self.factor))
            feature_indices.sort()
            self.features.append(feature_indices)
            self.clf[i].fit(x[:, feature_indices], y)

    def score(self, x, y):
        '''return the accuracy of prediction on testing data'''
        predictions = None
        for i in xrange(0, self.n_models):
            testing = x[:, self.features[i]]
            if predictions is None:
                predictions = self.clf[i].predict(testing)
            else:
                predictions = numpy.vstack((predictions, self.clf[i].predict(testing)))
        predictions = numpy.sign(predictions.transpose().sum(1))
        return numpy.mean(predictions == y)

def main():
    # initialize global data
    vec = TfidfVectorizer(ngram_range = (1, 5), strip_accents = None, charset_error = 'ignore', stop_words = None, min_df = 1)
    labels, stories = util.get_distress_data(config.CONNECTION)
    instances = vec.fit_transform(stories); labels = numpy.array(labels);
    random.seed(0)

    # cross validate
    n_models = 5; cv = 5; cv_accuracy = list();
    for i in xrange(0, cv):
        print "Iteration #" + str(i) + "..."

        # initialize training/testing data
        cv_data = cross_validation.train_test_split(instances, labels, test_size = 0.5, random_state = i)
        x_training = cv_data[0]
        x_testing = cv_data[1]
        y_training = cv_data[2]
        y_testing = cv_data[3]

        # initialize the classifier
        clf = BaggingSVM(n_models, 0.8)
        clf.fit(x_training, y_training)

        # measure prediction accuracy
        cv_accuracy.append(clf.score(x_testing, y_testing))

    print "Scores => " + str(cv_accuracy)
    print "Mean   => " + str(numpy.mean(cv_accuracy))

if __name__ == "__main__":
    main()
