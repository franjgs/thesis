#! /usr/bin/env python

import math, numpy, scipy, random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation
from sklearn.svm import SVC

import util

NUM_MODELS = 5

random.seed(1024)

class Stacking:

    def __init__(self, x_training, x_testing, y_training, y_testing, num_models):
        self.num_models = num_models
        # level 1
        self.x_training, self.y_training = x_training, y_training
        self.x_testing, self.y_testing = x_testing, y_testing
        self.models = list()
        # level 2
        self.instances, self.labels = None, None
        self.model = None

    def train(self):
        # train the models over the training data
        for i in xrange(0, self.num_models):
            model = SVC(C = 1)
            model.fit(self.x_training, self.y_training)
            self.models.append(model)
        # transform the training dataset to higher level
        x, y = None, None
        for i in xrange(0, self.num_models):
            if x is None:
                x = self.models[i].predict(self.x_training)
            else:
                x = scipy.vstack((x, self.models[i].predict(self.x_training)))
        x = x.transpose(); y = self.y_training;
        # train the second level model
        self.model = SVC(C = 1)
        self.model.fit(x, y)

    def test(self):
        # transform the testing data to higher level
        x, y = None, None
        for i in xrange(0, self.num_models):
            if x is None:
                x = self.models[i].predict(self.x_testing)
            else:
                x = scipy.vstack((x, self.models[i].predict(self.x_testing)))
        x = x.transpose(); y = self.y_testing;
        # return the accuracy
        predictions = self.model.predict(x)
        return float(sum(numpy.array(predictions.transpose())[0] == self.y_testing)) / float(len(self.y_testing))

def main():
    # initialize global data
    vec = TfidfVectorizer(ngram_range = (1, 2), stop_words = 'english')
    labels, _, comments = util.get_comments_data("Dataset/comments.csv")
    instances = vec.fit_transform(comments)

    cv = 5; cv_accuracy = list();
    for idx in xrange(0, cv):
        print "Iteration #" + str(idx) + "..."

        cv_data = cross_validation.train_test_split(instances, labels, test_size = 0.5, random_state = idx)
        x_training = cv_data[0]
        x_testing = cv_data[1]
        y_training = cv_data[2]
        y_testing = cv_data[3]

        stacking = Stacking(x_training, x_testing, y_training, y_testing, NUM_MODELS)
        stacking.train()
        cv_accuracy.append(stacking.test())

    print cv_accuracy

if __name__ == "__main__":
    main()
