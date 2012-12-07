#! /usr/bin/env python

import math, numpy, scipy, random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn import cross_validation

import util

NUM_MODELS = 5

random.seed(1024)

class Boosting:

    def __init__(self, x_training, x_testing, y_training, y_testing, num_models):
        self.x_training, self.y_training = x_training, y_training
        self.x_testing, self.y_testing = x_testing, y_testing
        n_samples, _ = x_training.get_shape()
        self.num_models = num_models
        self.models = list()
        self.w = (1.0 / n_samples) * numpy.matrix(numpy.ones(n_samples))
        self.alpha = numpy.matrix(numpy.zeros((self.num_models, 1)))
        self.eps = numpy.matrix(numpy.zeros((self.num_models, 1)))

    def train(self):
        for i in xrange(0, self.num_models):
            model = SVC(C = 1)
            model.fit(self.x_training, self.y_training, sample_weight = numpy.array(self.w)[0])
            I = numpy.matrix(map(lambda x: int(x), model.predict(self.x_training) != self.y_training))
            self.eps[i] = (self.w * I.transpose()) / self.w.sum(1)
            self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.multiply(self.w, scipy.exp(self.alpha[i] * I))
            self.models.append(model)

    def test(self):
        predictions = None
        for i in xrange(0, self.num_models):
            if predictions is None:
                predictions = self.models[i].predict(self.x_testing)
            else:
                predictions = scipy.vstack((predictions, self.models[i].predict(self.x_testing)))
        predictions = numpy.sign(predictions.transpose() * self.alpha)
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

        boosting = Boosting(x_training, x_testing, y_training, y_testing, NUM_MODELS)
        boosting.train()
        cv_accuracy.append(boosting.test())

    print cv_accuracy

if __name__ == "__main__":
    main()
