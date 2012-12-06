#! /usr/bin/env python

import util

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation

def main():
    labels, timestamps, comments = util.get_comments_data("Dataset/comments.csv")
    vec = TfidfVectorizer(ngram_range = (1, 2), stop_words = 'english')
    instances = vec.fit_transform(comments)

    clf = LinearSVC(C = 1)
    clf.fit(instances, labels)

    scores = cross_validation.cross_val_score(clf, instances, labels, cv = 5)
    print scores

if __name__ == "__main__":
    main()
