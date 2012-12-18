from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from numpy import where

class OnlineSVM(object):

    def __init__(self):
        self.model = None
        self.vec = None
        self.support_vectors = None

    def get_classifier(self):
        return SVC(C = 1, kernel = 'linear', class_weight = 'auto')

    def get_vectorizer(self):
        return TfidfVectorizer(ngram_range = (1, 2), min_df = 1, use_idf = True)

    def fit(self, comments, labels):
        '''fit the model to the first two samples'''
        self.model = self.get_classifier()
        self.vec = self.get_vectorizer()
        self.model.fit(self.vec.fit_transform(comments), labels)
        self.support_vectors = list()
        for i in xrange(0, 2):
            self.support_vectors.append([labels[i], comments[i]])

    def add(self, comment, label):
        '''update the model with the current sample, and return the prediction from the model before it was updated'''
        # current prediction
        prediction = self.model.predict(self.vec.transform([comment]))
        # append the current sample to the existing support vectors
        all_labels   = [i[0] for i in self.support_vectors] + [label]
        all_comments = [i[1] for i in self.support_vectors] + [comment]
        # convert the comments text to features
        self.vec = self.get_vectorizer()
        self.model = self.get_classifier()
        comments = self.vec.fit_transform(all_comments)
        self.model.fit(comments, all_labels)
        # update the list of support vectors
        support_vectors = self.model.support_vectors_.toarray()
        comments = comments.toarray()
        self.support_vectors = list()
        for sv in support_vectors:
            index = where((comments == sv).all(1) == True)[0][0]
            self.support_vectors.append([all_labels[index], all_comments[index]])
        # return the prediction obtained before the model was updated
        return prediction

