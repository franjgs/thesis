from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

class Base(object):
    
    def __init__(self):
        self.vec = None
    
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
        pass
    
    def predict(self, stories):
        pass
