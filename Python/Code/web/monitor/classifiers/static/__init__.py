from monitor.classifiers.static.svm import SVM
from monitor.classifiers.static.bagging import Bagging
from monitor.classifiers.static.boosting import Boosting
from monitor.classifiers.static.stacking import Stacking

from web import settings

class Classifiers(object):
    
    '''Util class to get/set global instances of classifiers'''
    
    svm = SVM()
    bagging = Bagging(n_models = settings.N_MODELS)
    boosting = Boosting(n_models = settings.N_MODELS)
    stacking = Stacking(n_models = settings.N_MODELS)
    
    __keys__ = [ 'svm', 'bagging', 'boosting', 'stacking' ]
    
    @classmethod
    def get(cls, key):
        if hasattr(cls, key):
            return getattr(cls, key)
        return None
    
    @classmethod
    def set(cls, key, value):
        if hasattr(cls, key):
            setattr(cls, key, value)
    
    @classmethod
    def all(cls):
        results = list()
        for key in cls.__keys__:
            results.append(getattr(cls, key))
        return results
    
    @classmethod
    def fit(cls, name, stories, labels):
        if name == "all":
            for key in cls.__keys__:
                clf = getattr(cls, key)
                clf.fit(stories, labels)
                setattr(cls, key, clf)
        else:
            if hasattr(cls, name):
                clf = getattr(cls, name)
                clf.fit(stories, labels)
                setattr(cls, key, clf)
