#! /usr/bin/env python

import util

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation
from pprint import pprint

def main():
    # initialize the global data
    labels, timestamps, comments = util.get_comments_data("Dataset/comments.csv")
    vec = TfidfVectorizer(ngram_range = (1, 2), stop_words = 'english')
    instances = vec.fit_transform(comments)

    cv = 5; cv_accuracy = list();
    for idx in xrange(0, cv):
        # initialize training/testing data
        cv_data = cross_validation.train_test_split(instances, labels, test_size = 0.5, random_state = idx)
        x_training = cv_data[0]
        x_testing = cv_data[1]
        y_training = cv_data[2]
        y_testing = cv_data[3]

        # train the classifier on the training data
        clf = LinearSVC(C = 1)
        clf.fit(x_training, y_training)

        # test the classifer on the testing data
        predictions = clf.predict(x_testing)
        correct = sum(predictions == y_testing)
        total = len(predictions)
        cv_accuracy.append(float(correct) / float(total))

    pprint(cv_accuracy)

if __name__ == "__main__":
    main()
