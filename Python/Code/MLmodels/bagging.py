#! /usr/bin/env python

import numpy, random, scipy

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation

import util

NUM_MODELS = 5

random.seed(1024)

def main():
    # initialize global data
    vec = TfidfVectorizer(ngram_range = (1, 2), stop_words = 'english')
    labels, _, comments = util.get_comments_data("Dataset/comments.csv")
    instances = vec.fit_transform(comments)

    cv = 5; cv_accuracy = list();
    for idx in xrange(0, cv):
        print "Iteration #" + str(idx) + "..."

        # initialize training/testing data
        cv_data = cross_validation.train_test_split(instances, labels, test_size = 0.5, random_state = idx)
        x_training = cv_data[0]
        x_testing = cv_data[1]
        y_training = cv_data[2]
        y_testing = cv_data[3]

        n_samples, n_features = x_training.get_shape()

        # train the classifiers on training data
        models, features = list(), list();
        for i in xrange(0, NUM_MODELS):
            # pick a random subset of features to be used to train this model
            feature_indices = random.sample(xrange(0, n_features), n_features / NUM_MODELS)
            feature_indices.sort()
            training = x_training[:, feature_indices]
            # train the model
            model = LinearSVC(C = 1)
            model.fit(training, y_training)
            models.append(model)
            # store the feature indices
            features.append(feature_indices)

        # test the classifiers on the testing data
        predictions = None
        for i in xrange(0, NUM_MODELS):
            # build the data (with only the features assigned to this model)
            testing = x_testing[:, features[i]]
            if predictions is None:
                predictions = models[i].predict(testing)
            else:
                predictions = scipy.vstack((predictions, models[i].predict(testing)))
        predictions = numpy.sign(predictions.transpose().sum(1))

        # measure the accuracy
        cv_accuracy.append(float(sum(predictions == y_testing)) / float(len(y_testing)))

        print "Done!"

    print cv_accuracy

if __name__ == "__main__":
    main()

