#! /usr/bin/env python

import random
random.seed(0)

from lib import util

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation
from sklearn.svm import SVC
import math, numpy, scipy

class StackingSVM:
    def __init__(self, num_models):
        self.num_models = num_models
        # first level classifiers
        self.models = list()
        for i in xrange(0, self.num_models):
            self.models.append(SVC(C = i + 1, kernel = 'linear', class_weight = 'auto'))
        # second level classifiers
        self.model = None
    def fit(self, x, y):
        # train all the first level classifiers
        for i in xrange(0, self.num_models):
            self.models[i].fit(x, y)
        # transform the training dataset to second level
        training = None
        for i in xrange(0, self.num_models):
            if training is None:
                training = self.models[i].predict(x)
            else:
                training = scipy.vstack((training, self.models[i].predict(x)))
        training = training.transpose()
        # train the second level model
        self.model = SVC(C = 1, kernel = 'linear', class_weight = 'auto')
        self.model.fit(training, y)
    def score(self, x, y):
        # convert the testing dataset to second level
        testing = None
        for i in xrange(0, self.num_models):
            if testing is None:
                testing = self.models[i].predict(x)
            else:
                testing = scipy.vstack((testing, self.models[i].predict(x)))
        testing = testing.transpose()
        # measure the predictions and return accuracy
        return numpy.mean(self.model.predict(testing) == y)

def main():
    # initialize global data
    vec = TfidfVectorizer(ngram_range = (1, 2), stop_words = 'english')
    labels, _, comments = util.get_comments_data("Dataset/comments.csv")
    instances = vec.fit_transform(comments)

    num_models = 5; cv = 5; cv_accuracy = list();
    for i in xrange(0, cv):
        print "Iteration #" + str(i) + "..."

        # initialize training/testing data
        cv_data = cross_validation.train_test_split(instances, labels, test_size = 0.5, random_state = i)
        x_training = cv_data[0]
        x_testing = cv_data[1]
        y_training = cv_data[2]
        y_testing = cv_data[3]

        # initialize the classifier
        clf = StackingSVM(num_models)
        clf.fit(x_training, y_training)

        # measure prediction accuracy
        cv_accuracy.append(clf.score(x_testing, y_testing))

    print "Scores => " + str(cv_accuracy)
    print "Mean   => " + str(numpy.mean(cv_accuracy))

if __name__ == "__main__":
    main()

