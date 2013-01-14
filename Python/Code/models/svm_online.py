#! /usr/bin/env python

import sys

from lib import util, config
from lib.online_text_svm import OnlineTextSVM

def main():
    # initial setup
    labels, stories = util.get_distress_data(config.CONNECTION)
    clf = OnlineTextSVM(randomize = False)
    total, correct = 0.0, 0.0

    # input first two samples (having different labels), and then continue with the online mode
    positive, negative = labels.index(1), labels.index(-1)
    clf.fit( [stories[positive], stories[negative]], [labels[positive], labels[negative]] )
    indices = [i for i in xrange(0, len(labels)) if i not in [positive, negative]]
    for i in indices:
        prediction = clf.predict(stories[i])
        clf.add(stories[i], labels[i])
        if prediction == labels[i]:
            correct = correct + 1
        total = total + 1
        print "#%d => (Cumulative accuracy, Support Vectors) = (%.3f, %d)" % (i, correct / total, clf.get_sv_count())

if __name__ == "__main__":
    main()