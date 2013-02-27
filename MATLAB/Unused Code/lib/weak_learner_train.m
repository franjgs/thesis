function [model] = weak_learner_train(method, x, y, classifier, options)
    model = cell(2, 1);
    if strcmp(method, 'bagging') == 1
        % bagging requires individual models to be trained on a random
        % subset of the data
        n = size(x, 1);
        indices = randsample(n, randi([round(n/2), n]));
        x = x(indices, :);
        y = y(indices, :);
    elseif strcmp(method, 'subset_of_features') == 1
        % train a model on a random subset of the features, while setting
        % all the other feature values to 0
        n = size(x, 2);
        features_chosen = randsample(n, randi([1,round(n/10)]));
        features_leftout = setdiff((1: n), features_chosen);
        x(:, features_leftout) = 0;
    end
    if strcmp(classifier, 'svm') == 1
        positive = size(y, 1) / sum(y == 1);
        negative = size(y, 1) / sum(y == -1);
        w = ones(size(x, 1), 1);
        if nargin == 4
            % no options; use linear kernel and add class weights
            params = sprintf('-t 0 -w1 %.2f -w-1 %.2f', positive, negative);
        else
            % options given; just add class weights
            params = sprintf('%s -w1 %.2f -w-1 %.2f', options, positive, negative);
        end
        model{1} = svmtrain(w, y, x, params);
        model{2} = 'svm';
        fprintf('Trained an SVM with param => %s\n', params);
    elseif strcmp(classifier, 'tree') == 1
        model{1} = ClassificationTree.fit(full(x), y);
        model{2} = 'tree';
    elseif strcmp(classifier, 'naivebayes') == 1
        model{1} = NaiveBayes.fit(x, y);
        model{2} = 'naivebayes';
    end
end
