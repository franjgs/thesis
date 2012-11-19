clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/a1a.data');

n_global = size(labels, 1);
cv = 5;
cv_accuracy = zeros(1, cv);

features_total = size(instances, 2);
features_per_learner = 2;
num_learners = round(features_total / features_per_learner);

for idx = 1 : cv
    fprintf('Iteration #%d\n', idx);
    
    testing = randsample(n_global, round(n_global/cv));
    training = setdiff((1: n_global), testing)';
    
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
        learners{i} = weak_learner_train('boosting', x_training(:, feature_indices), y_training, 'tree');
        % calculate the classifier accuracy on the training data
        clf_accuracy(i, :) = sum(weak_learner_predict(x_training(:, feature_indices), y_training, learners{i}{1}, learners{i}{2}) == y_training) / size(y_training, 1);
        % remove the features from the original training data
        x_training(:, feature_indices) = [];
    end
    fprintf('Done\n');
    
    predictions = random_subspace_predict(x_testing, learners, features, clf_accuracy);
    
    cv_accuracy(idx) = sum(predictions == y_testing) / size(y_testing, 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
