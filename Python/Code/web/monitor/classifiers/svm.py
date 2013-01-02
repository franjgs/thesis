import numpy
from monitor.classifiers.lib.online_text_svm import OnlineTextSVM

class SVM(object):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SVM, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.clf = None

    def get_classifier(self):
        return OnlineTextSVM(randomize = False)

    def predict(self, story):
        '''return the prediction from the current model'''
        return self.clf.predict(story)

    def fit(self, stories, labels):
        '''fit the model to the first few samples'''
        if self.clf is None:
            self.clf = self.get_classifier()
        self.clf.fit(stories, labels)

    def add(self, story, label):
        '''update the model with the current sample'''
        self.clf.add(story, label)
