import numpy
from monitor.classifiers.lib.online_text_svm import OnlineTextSVM

class Bagging(object):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Bagging, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, n_models):
        self.n_models = n_models
        self.clf = list()

    def get_classifier(self):
        return OnlineTextSVM(randomize = True, factor = 0.5)

    def predict(self, story):
        '''return the prediction from the current set of models'''
        predictions = list()
        for i in xrange(0, self.n_models):
            predictions.append(self.clf[i].predict(story))
        return numpy.sign(sum(predictions))

    def fit(self, stories, labels):
        '''fit all the models to the first few samples'''
        for i in xrange(0, self.n_models):
            self.clf.append(self.get_classifier())
            self.clf[i].fit(stories, labels)

    def add(self, story, label):
        '''update all the models with the current sample'''
        for i in xrange(0, self.n_models):
            self.clf[i].add(story, label)

