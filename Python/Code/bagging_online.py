#! /usr/bin/env python

from lib.util import get_comments_data

class OnlineBagging:

    def __init__(self, num_models):
        self.num_models
        self.models = [None] * self.num_models
        self.vec = [None] * self.num_models
        self.features = [None] * self.num_models
        self.support_vectors = [None] * self.num_models

    def get_classifier(self):
        return SVC(C = 1, kernel = 'linear', class_weight = 'auto')

    def get_vectorizer(self):
        return TfidfVectorizer(ngram_range = (1, 2), min_df = 1, use_idf = True)

    def fit(self, comments, labels):
        '''TODO: fit all the models to the first two samples'''
        pass

    def add(self, comment, label):
        '''TODO: update the model with the current sample, and return the prediction from the model before it was updated'''
        pass

def main(filename):
    # initial setup
    labels, _, comments = get_comments_data(filename)
    clf = OnlineBagging()

    # input first two samples (having different labels), and then continue with the online mode
    positive, negative = labels.index(1), labels.index(-1)
    clf.fit( [comments[positive], comments[negative]], [labels[positive], labels[negative]] )
    indices = [i for i in xrange(0, len(labels)) if i not in [positive, negative]]
    for i in indices:
        clf.add(comments[i], labels[i])

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        print "Usage: python %s <training_file>" % sys.argv[0]
    else:
        main(filename)
