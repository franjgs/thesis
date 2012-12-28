import numpy, random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

class OnlineTextSVM(object):

    '''
    An implementation of an online Support Vector Machine, used for text input
    For each new sample, retraining is done only on the set of support vectors plus the new sample
    '''

    def __init__(self, randomize = False, factor = 0.3):
        self.clf = None
        self.vec = None
        self.support_vectors_x = None
        self.support_vectors_y = None
        self.randomize = randomize
        if randomize is not False:
            self.indices = None
            self.factor = factor

    def get_classifier(self):
        return SVC(C = 1, kernel = 'linear', class_weight = 'auto')

    def get_vectorizer(self):
        return TfidfVectorizer(ngram_range = (1, 5), min_df = 1, strip_accents = None, charset_error = 'ignore', stop_words = None)

    def fit(self, stories, labels, sample_weight = None):
        '''fit the classifier to the first samples'''
        self.clf = self.get_classifier()
        self.vec = self.get_vectorizer()
        x = self.vec.fit_transform(stories); y = numpy.array(labels);
        n_samples, n_features = x.get_shape()
        if self.randomize:
            self.indices = random.sample(xrange(0, n_features), int(n_features * self.factor))
            self.indices.sort()
            x = x[:, self.indices]
        self.clf.fit(x, y, sample_weight = sample_weight)
        self.support_vectors_x = list()
        self.support_vectors_y = list()
        support_vectors = self.clf.support_vectors_.toarray()
        x = x.toarray()
        for sv in support_vectors:
            index = numpy.where((x == sv).all(1) == True)[0][0]
            self.support_vectors_x.append(stories[index])
            self.support_vectors_y.append(labels[index])

    def predict(self, story):
        '''return the prediction from the current classifier'''
        if self.clf is None or self.vec is None:
            return None
        if type(story) == str:
            x = self.vec.transform([story])
        else:
            x = self.vec.transform(story)
        if self.randomize and self.indices:
            x = x[:, self.indices]
        return self.clf.predict(x)

    def add(self, story, label):
        '''update the classifier with the current sample'''
        # append the current sample to the existing support vectors
        all_labels      = self.support_vectors_y + [label]
        all_stories     = self.support_vectors_x + [story]
        # convert the stories text to features
        self.vec = self.get_vectorizer()
        self.clf = self.get_classifier()
        x = self.vec.fit_transform(all_stories); y = numpy.array(all_labels);
        if self.randomize:
            n_samples, n_features = x.get_shape()
            self.indices = random.sample(xrange(0, n_features), int(n_features * self.factor))
            self.indices.sort()
            x = x[:, self.indices]
        self.clf.fit(x, y)
        # update the list of support vectors
        support_vectors = self.clf.support_vectors_.toarray()
        stories = x.toarray()
        self.support_vectors_x = list()
        self.support_vectors_y = list()
        for sv in support_vectors:
            index = numpy.where((stories == sv).all(1) == True)[0][0]
            self.support_vectors_x.append(all_stories[index])
            self.support_vectors_y.append(all_labels[index])

