from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from monitor.classifiers.static.base import Base

class SVM(Base):
    
    '''Thin wrapper around the sklearn SVM classifier'''
    
    def __init__(self):
        self.clf = None
        super(SVM, self).__init__()
    
    def fit(self, stories, labels):
        self.vec = self.get_vectorizer()
        self.clf = self.get_classifier()
        self.clf.fit(self.vec.fit_transform(stories), labels)
    
    def predict(self, stories):
        if self.vec is None or self.clf is None:
            return None
        if type(stories) == str:
            stories = [stories]
        return self.clf.predict(self.vec.transform(stories))
