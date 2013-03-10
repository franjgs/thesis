import random
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from monitor.classifiers.static.base import Base

class Bagging(Base):
    
    '''Thin wrapper around multiple SVMs to implement bagging'''
    
    def __init__(self, n_models):
        self.n_models   = n_models
        self.clf        = list()
        super(Bagging, self).__init__()
    
    def fit(self, stories, labels):
        self.vec = self.get_vectorizer()
        x = self.vec.fit_transform(stories); y = numpy.array(labels);
        n_samples = x.get_shape()[0]
        for i in xrange(0, self.n_models):
            indices = random.sample(xrange(0, n_samples), random.randrange(n_samples / 2, n_samples))
            clf = self.get_classifier()
            clf.fit(x[indices, :], y[indices, :])
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
        predictions = numpy.sign(predictions.transpose().sum(1))
        return predictions
