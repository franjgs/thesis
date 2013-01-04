from monitor.classifiers.svm import SVM
from monitor.classifiers.bagging import Bagging
from monitor.classifiers.boosting import Boosting
from monitor.classifiers.stacking import Stacking

from ratings.models import Story

from web import settings

def initialize():
    labels, stories = list(), list()
    for story in Story.objects.exclude(label = 0):
        labels.append(int(story.label))
        stories.append(story.content)
    for model in [SVM, Bagging, Boosting, Stacking]:
        print "Initializing " + model.__name__
        clf = None
        if model == SVM:
            clf = model()
        else:
            clf = model(n_models = 5)
        clf.fit(stories, labels)
        settings.CLASSIFIERS[model.__name__] = clf
        print "Done!"
