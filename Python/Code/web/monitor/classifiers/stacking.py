import numpy
from monitor.classifiers.lib.online_svm import OnlineSVM
from monitor.classifiers.lib.online_text_svm import OnlineTextSVM

class Stacking(object):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Stacking, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, n_models):
        self.n_models = n_models
        self.models = list()
        self.clf = None

    def get_classifier(self, level):
        if level == 1:
            return OnlineTextSVM(randomize = False)
        elif level == 2:
            return OnlineSVM(randomize = False)

    def predict(self, story):
        '''return the prediction from the current set of models'''
        # calculate the input for the second level classifier
        x = None
        for i in xrange(0, self.n_models):
            if x is None:
                x = self.models[i].predict(story)
            else:
                x = numpy.vstack((x, self.models[i].predict(story)))
        x = x.transpose()
        return self.clf.predict(x)

    def fit(self, stories, labels):
        '''fit all the models to the first few samples'''
        # train the first level models
        for i in xrange(0, self.n_models):
            self.models.append(self.get_classifier(level = 1))
            self.models[i].fit(stories, labels)
        # convert the data to second level training data
        x = None
        for i in xrange(0, self.n_models):
            if x is None:
                x = self.models[i].predict(stories)
            else:
                x = numpy.vstack((x, self.models[i].predict(stories)))
        x = x.transpose()
        # train the second level model
        self.clf = self.get_classifier(level = 2)
        self.clf.fit(x, labels)

    def add(self, story, label):
        '''update all the models with the current sample'''
        for i in xrange(0, self.n_models):
            self.models[i].add(story, label)
        x = None
        for i in xrange(0, self.n_models):
            if x is None:
                x = self.models[i].predict(story)
            else:
                x = numpy.vstack((x, self.models[i].predict(story)))
        x = x.transpose()
        self.clf.add(x, label)

