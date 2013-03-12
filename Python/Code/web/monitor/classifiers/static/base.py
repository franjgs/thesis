from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

class Base(object):
    
    def __init__(self):
        self.vec = None
    
    def get_name(self):
        return self.__class__.__name__.lower()
    
    def get_vectorizer(self):
        return TfidfVectorizer(
            ngram_range = (1, 2),
            min_df = 2,
            strip_accents = None,
            charset_error = 'ignore',
            stop_words = None
        )
    
    def get_classifier(self, kernel = 'linear'):
        return SVC(
            C = 1,
            kernel = kernel,
            class_weight = 'auto'
        )
    
    def fit(self, stories, labels):
        pass
    
    def predict(self, stories):
        pass
