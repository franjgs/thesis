clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/a1a.data');

n_global = size(labels, 1);
cv = cvpartition(labels, 'HoldOut', 0.5);
cv_accuracy = zeros(1, cv.NumTestSets);

features_total = size(instances, 2);
features_per_learner = 2;
num_learners = round(features_total / features_per_learner);
param = '-t 0 -c 1 -h 0 -w1 %.3f -w-1 %.3f';

for idx = 1 : cv.NumTestSets
    fprintf('Iteration #%d\n', idx);
    
    training = cv.training(idx);
    testing = cv.test(idx);
    
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    
    fprintf('Training learners...');
    learners = cell(num_learners, 1);
    features = cell(num_learners, 1);
    clf_accuracy = zeros(num_learners, 1);
    for i = 1 : num_learners
        % pick a random set of features
        if size(x_training, 2) < features_per_learner
            feature_indices = (1: size(x_training, 2))';
        else
            feature_indices = randsample(size(x_training, 2), features_per_learner);
        end
        % store these feature indices corresponding to this learner
        features{i} = feature_indices;
        % train a weak learner on this set of features
        positive = numel(y_training) / sum(y_training == 1);
        negative = numel(y_training) / sum(y_training == -1);
        learners{i} = svmtrain(ones(numel(y_training), 1), y_training, x_training(:, feature_indices), sprintf(param, positive, negative));
        % calculate the classifier accuracy on the training data
        clf_accuracy(i, :) = sum(svmpredict(y_training, x_training(:, feature_indices), learners{i}) == y_training) / size(y_training, 1);
        % remove the features from the original training data
        x_training(:, feature_indices) = [];
    end
    fprintf('Done\n');
    
    % given the learners, and the feature indices these learners work on
    % obtain predictions from all the learners, and take a weighted vote
    n = size(x_testing, 1);
    predictions = zeros(n, num_learners);
    for i = 1 : num_learners
        predictions(:, i) = svmpredict(zeros(n, 1), x_testing(:, features{i}), learners{i});
    end
    predictions = sign(predictions * clf_accuracy);
    
    cv_accuracy(idx) = sum(predictions == y_testing) / size(y_testing, 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
