import numpy
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

class Stacking(object):
    
    '''Thin wrapper around multiple SVMs to implement Stacking'''
    
    def __init__(self, n_models):
        self.n_models   = n_models
        self.models     = list()
        self.indices    = list()
        self.vec        = None
        self.clf        = None
    
    def get_vectorizer(self):
        return TfidfVectorizer(
            ngram_range = (1, 5),
            min_df = 1,
            strip_accents = None,
            charset_error = 'ignore',
            stop_words = None
        )
    
    def get_classifier(self):
        return SVC(
            C = 1,
            kernel = 'linear',
            class_weight = 'auto'
        )
    
    def fit(self, stories, labels):
        self.vec = self.get_vectorizer()
        x = self.vec.fit_transform(stories)
        # train the first level classifiers
        n_samples, n_features = x.get_shape()
        for i in xrange(0, self.n_models):
            model = self.get_classifier()
            indices = random.sample(xrange(0, n_features), int(n_features / self.n_models))
            indices.sort()
            model.fit(x[:, features], y)
            self.indices.append(indices)
            self.models.append(model)
        # train the second level classifiers
        training = None
        for i in xrange(0, self.n_models):
            if training is None:
                training = self.models[i].predict(x[:, self.features[i]])
            else:
                training = numpy.vstack((training, self.models[i].predict(x[:, self.features[i]])))
        training = training.transpose()
        self.clf = self.get_classifier()
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
                testing = self.models[i].predict(x[:, self.features[i]])
            else:
                testing = numpy.vstack((testing, self.models[i].predict(x[:, self.features[i]])))
        testing = testing.transpose()
        return self.clf.predict(testing)
