import numpy
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from monitor.classifiers.static.base import Base

class Stacking(Base):
    
    '''Thin wrapper around multiple SVMs to implement Stacking'''
    
    def __init__(self, n_models):
        self.n_models   = n_models
        self.models     = list()
        self.clf        = None
        super(Stacking, self).__init__()
    
    def fit(self, stories, labels):
        self.vec = self.get_vectorizer()
        x = self.vec.fit_transform(stories); y = numpy.array(labels);
        # train the first level classifiers
        n_samples = x.get_shape()[0]
        for i in xrange(0, self.n_models):
            model = self.get_classifier()
            indices = random.sample(xrange(0, n_samples), random.randrange(n_samples / 2, n_samples))
            model.fit(x[indices, :], y[indices, :])
            self.models.append(model)
        # train the second level classifier
        training = None
        for i in xrange(0, self.n_models):
            if training is None:
                training = self.models[i].predict(x)
            else:
                training = numpy.vstack((training, self.models[i].predict(x)))
        training = training.transpose()
        self.clf = self.get_classifier('rbf')
        self.clf.fit(training, y)
    
    def predict(self, stories):
        if self.vec is None or len(self.models) == 0 or self.clf is None:
            return None
        if type(stories) == str:
            stories = [stories]
        x = self.vec.transform(stories)
        testing = None
        for i in xrange(0, self.n_models):
            if testing is None:
                testing = self.models[i].predict(x)
            else:
                testing = numpy.vstack((testing, self.models[i].predict(x)))
        testing = testing.transpose()
        return self.clf.predict(testing)
