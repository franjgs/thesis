#! /usr/bin/env python

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from pprint import pprint
import numpy, sys

from lib import util

class OnlineSVM(object):

    def __init__(self):
        self.model = None
        self.vec = None
        self.support_vectors = None

    def get_classifier(self):
        return SVC(C = 1, kernel = 'linear', class_weight = 'auto')

    def get_vectorizer(self):
        return TfidfVectorizer(ngram_range = (1, 2), min_df = 1, use_idf = True)

    def add(self, comments, labels):
        '''fit the model to the first two samples'''
        self.model = self.get_classifier()
        self.vec = self.get_vectorizer()
        self.model.fit(self.vec.fit_transform(comments), labels)
        self.support_vectors = list()
        for i in xrange(0, 2):
            self.support_vectors.append([labels[i], comments[i]])

    def fit(self, comment, label):
        '''update the model with the current sample'''
        # append the current sample to the existing support vectors
        all_labels   = [i[0] for i in self.support_vectors] + [label]
        all_comments = [i[1] for i in self.support_vectors] + [comment]
        # convert the comments text to features
        self.vec = self.get_vectorizer()
        self.model = self.get_classifier()
        comments = self.vec.fit_transform(all_comments)
        self.model.fit(comments, all_labels)
        # update the list of support vectors
        support_vectors = self.model.support_vectors_.toarray()
        comments = comments.toarray()
        self.support_vectors = list()
        for sv in support_vectors:
            index = numpy.where((comments == sv).all(1) == True)[0][0]
            self.support_vectors.append([all_labels[index], all_comments[index]])

def main(filename):
    # initial setup
    labels, _, comments = util.get_comments_data(filename)
    clf = OnlineSVM()

    # input first two samples (having different labels), and then continue with the online mode
    positive, negative = labels.index(1), labels.index(-1)
    clf.add( [comments[positive], comments[negative]], [labels[positive], labels[negative]] )
    indices = [i for i in xrange(0, len(labels)) if i not in [positive, negative]]
    for i in indices:
        print "index %d (n_sv = %d)" % (i, len(clf.support_vectors))
        clf.fit(comments[i], labels[i])

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        print "Usage: python %s <training_file>" % sys.argv[0]
    else:
        main(filename)
