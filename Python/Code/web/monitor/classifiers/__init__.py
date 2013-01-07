from monitor.classifiers.online.svm import OnlineSVM
from monitor.classifiers.online.bagging import OnlineBagging
from monitor.classifiers.online.boosting import OnlineBoosting
from monitor.classifiers.online.stacking import OnlineStacking

models = [OnlineSVM, OnlineBagging, OnlineBoosting, OnlineStacking]
