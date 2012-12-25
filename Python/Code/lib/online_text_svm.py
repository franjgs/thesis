import numpy, random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

class OnlineTextSVM(object):

    '''
    An implementation of an online Support Vector Machine
    For each new sample, retraining is done only on the set of support vectors plus the new sample
    '''

    def __init__(self, randomize = False, factor = 0.5):
        self.clf = None
        self.vec = None
        self.support_vectors = None
        self.randomize = randomize
        if randomize is not False:
            self.indices = None
            self.factor = factor

    def get_classifier(self):
        return SVC(C = 1, kernel = 'linear', class_weight = 'auto')

    def get_vectorizer(self):
        return TfidfVectorizer(ngram_range = (1, 2), min_df = 1, use_idf = True)

    def fit(self, comments, labels, sample_weight = None):
        '''fit the classifier to the first two samples'''
        assert(len(comments) == 2)
        assert(len(labels) == 2)
        self.clf = self.get_classifier()
        self.vec = self.get_vectorizer()
        x = self.vec.fit_transform(comments); y = labels;
        if self.randomize:
            total_features = x.get_shape()[1]
            self.indices = random.sample(xrange(0, total_features), int(total_features * self.factor))
            self.indices.sort()
            x = x[:, self.indices]
        self.clf.fit(x, y, sample_weight = sample_weight)
        self.support_vectors = list()
        for i in xrange(0, 2):
            self.support_vectors.append([labels[i], comments[i]])

    def predict(self, comment):
        '''return the prediction from the current classifier'''
        if self.clf is None or self.vec is None:
            return None
        if type(comment) == str:
            x = self.vec.transform([comment])
        else:
            x = self.vec.transform(comment)
        if self.randomize and self.indices:
            x = x[:, self.indices]
        return self.clf.predict(x)

    def add(self, comment, label):
        '''update the classifier with the current sample'''
        # append the current sample to the existing support vectors
        all_labels   = [i[0] for i in self.support_vectors] + [label]
        all_comments = [i[1] for i in self.support_vectors] + [comment]
        # convert the comments text to features
        self.vec = self.get_vectorizer()
        self.clf = self.get_classifier()
        x = self.vec.fit_transform(all_comments); y = all_labels;
        if self.randomize:
            total_features = x.get_shape()[1]
            self.indices = random.sample(xrange(0, total_features), int(total_features * self.factor))
            self.indices.sort()
            x = x[:, self.indices]
        self.clf.fit(x, y)
        # update the list of support vectors
        support_vectors = self.clf.support_vectors_.toarray()
        comments = x.toarray()
        self.support_vectors = list()
        for sv in support_vectors:
            index = numpy.where((comments == sv).all(1) == True)[0][0]
            self.support_vectors.append([all_labels[index], all_comments[index]])

