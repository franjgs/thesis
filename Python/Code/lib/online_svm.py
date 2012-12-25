import numpy
import scipy
import random
from sklearn.svm import SVC

class OnlineSVM(object):
    '''
    An implementation of an online Support Vector Machine
    For each new sample, retraining is done only on the set of support vectors plus the new sample
    '''

    def __init__(self, randomize = False, factor = 0.5):
        self.clf = None
        self.vec = None
        self.support_vectors = None
        self.randomize = randomize
        if randomize is not False:
            self.factor = factor

    def get_classifier(self):
        return SVC(C = 1, kernel = 'linear', class_weight = 'auto')

    def fit(self, x, y, sample_weight = None):
        '''fit the classifier to the first two samples'''
        self.clf = self.get_classifier()
        if self.randomize:
            total_features = x.get_shape()[1]
            self.indices = random.sample(xrange(0, total_features), int(total_features * self.factor))
            self.indices.sort()
            x = x[:, self.indices]
        self.clf.fit(x, y, sample_weight = sample_weight)
        self.support_vectors_x = self.clf.support_vectors_
        self.support_vectors_y = self.clf.predict(self.support_vectors_x)

    def predict(self, x):
        '''return the prediction from the current classifier'''
        if self.clf is None:
            return None
        if self.randomize and self.indices:
            x = x[:, self.indices]
        return self.clf.predict(x)

    def add(self, x, y):
        '''update the classifier with the current sample'''
        # append the current sample to the existing support vectors
        x = scipy.sparse.vstack((self.support_vectors_x, scipy.matrix(x)))
        y = numpy.hstack((self.support_vectors_y, numpy.array(y)))
        # fit the data to the model
        self.clf = self.get_classifier()
        if self.randomize:
            total_features = x.get_shape()[1]
            self.indices = random.sample(xrange(0, total_features), int(total_features * self.factor))
            self.indices.sort()
            x = x[:, self.indices]
        self.clf.fit(x, y)
        # update the list of support vectors
        self.support_vectors_x = self.clf.support_vectors_
        self.support_vectors_y = self.clf.predict(self.support_vectors_x)

