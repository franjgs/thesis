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
        self.indices    = list()
        super(Bagging, self).__init__()
    
    def fit(self, stories, labels):
        self.vec = self.get_vectorizer()
        x = self.vec.fit_transform(stories)
        n_samples, n_features = x.get_shape()
        for i in xrange(0, self.n_models):
            indices = random.sample(xrange(0, n_features), int(n_features / self.n_models))
            indices.sort()
            clf = self.get_classifier()
            clf.fit(x[:, indices], labels)
            self.indices.append(indices)
            self.clf.append(clf)
    
    def predict(self, stories):
        if self.vec is None or len(self.clf) == 0:
            return None
        if type(stories) == str:
            stories = [stories]
        x = self.vec.transform(stories)
        predictions = None
        for i in xrange(0, self.n_models):
            testing = x[:, self.indices[i]]
            if predictions is None:
                predictions = self.clf[i].predict(testing)
            else:
                predictions = numpy.vstack((predictions, self.clf[i].predict(testing)))
        predictions = numpy.sign(predictions.transpose().sum(1))
        return predictions
