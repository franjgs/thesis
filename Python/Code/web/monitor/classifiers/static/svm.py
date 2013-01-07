from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

class SVM(object):
    
    '''Thin wrapper around the sklearn SVM classifier'''
    
    def __init__(self):
        self.vec = None
        self.clf = None
    
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
        self.clf = self.get_classifier()
        self.clf.fit(self.vec.fit_transform(stories), labels)
    
    def predict(self, stories):
        if self.vec is None or self.clf is None:
            return None
        if type(stories) == str:
            stories = [stories]
        return self.clf.predict(self.vec.transform(stories))
