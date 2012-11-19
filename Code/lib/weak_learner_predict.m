function [labels] = weak_learner_predict(x, y, model, method)
    if strcmp(method, 'svm') == 1
        labels = svmpredict(y, x, model);
    elseif strcmp(method, 'tree') == 1
        labels = model.predict(full(x));
    elseif strcmp(method, 'naivebayes') == 1
        labels = model.predict(x);
    end
end
