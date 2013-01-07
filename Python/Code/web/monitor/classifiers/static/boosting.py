import numpy
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from monitor.classifiers.static.base import Base

class Boosting(Base):
    
    '''Thin wrapper around multiple SVMs to implement Boosting'''
    
    def __init__(self, n_models):
        self.n_models   = n_models
        self.clf        = list()
        self.w          = None
        self.alpha      = numpy.matrix(numpy.zeros((self.n_models, 1)))
        self.eps        = numpy.matrix(numpy.zeros((self.n_models, 1)))
        super(Boosting, self).__init__()
    
    def fit(self, stories, labels):
        self.vec = self.get_vectorizer()
        x = self.vec.fit_transform(stories)
        n_samples, n_features = x.get_shape()
        self.w = (1.0 / n_samples) * numpy.matrix(numpy.ones(n_samples))
        for i in xrange(0, self.n_models):
            clf = self.get_classifier()
            clf.fit(x, y, sample_weight = numpy.array(self.w[-1, :])[0])
            I = numpy.matrix(map(lambda f: int(f), clf.predict(x) != y))
            self.eps[i] = (self.w[-1, :] * I.transpose()) / self.w[-1, :].sum(1)
            if self.eps[i] == 0:
                self.alpha[i] = 1
            else:
                self.alpha[i] = math.log((1 - self.eps[i]) / self.eps[i])
            self.w = numpy.vstack((self.w, (numpy.multiply(self.w[-1, :], numpy.exp(self.alpha[i] * I)))))
            self.clf.append(clf)
    
    def predict(self, stories):
        if self.vec is None or len(self.clf) == 0:
            return None
        if type(stories) == str:
            stories = [stories]
        x = self.vec.transform(stories)
        predictions = None
        for i in xrange(0, self.n_models):
            if predictions is None:
                predictions = self.clf[i].predict(x)
            else:
                predictions = numpy.vstack((predictions, self.clf[i].predict(x)))
        predictions = numpy.sign(predictions.transpose() * self.alpha)
        return predictions
