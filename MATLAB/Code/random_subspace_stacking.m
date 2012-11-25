clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/a1a.data');

n_global = size(instances, 1);
cv = 5;
cv_accuracy = zeros(1, cv);
param = '-t 0 -c 1 -h 0 -w1 %.3f -w-1 %.3f';

features_per_learner = 10;
num_features = size(instances, 2);
num_learners = round(num_features / features_per_learner);

for idx = 1 : cv
    fprintf('Iteration #%d\n', idx);
    
    testing = randsample(n_global, round(n_global/cv));
    training = setdiff((1: n_global), testing)';
    
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    
    fprintf('Training %d learners...', num_learners);
    learners = cell(num_learners, 1);
    features = cell(num_learners, 1);
    for i = 1 : num_learners
        % pick out random features
        if size(x_training, 2) < features_per_learner
            feature_indices = (1: size(x_training, 2))';
        else
            feature_indices = randsample(size(x_training, 2), features_per_learner);
        end
        features{i} = feature_indices;
        % train the learners on these features
        positive = numel(y_training) / sum(y_training == 1);
        negative = numel(y_training) / sum(y_training == -1);
        learners{i} = svmtrain(ones(numel(y_training), 1), y_training, x_training(:, features{i}), sprintf(param, positive, negative));
        % remove the features from the training data
        x_training(:, feature_indices) = [];
    end
    fprintf('Done\n');
    
    % transform the data into the new dimensional space
    x = zeros(n_global, num_learners);
    y = labels;
    for i = 1 : num_learners
        x(:, i) = svmpredict(labels, instances(:, features{i}), learners{i});
    end
    
    % train a new learner on this new dimensional space
    positive = numel(y(training, :)) / sum(y(training, :) == 1);
    negative = numel(y(training, :)) / sum(y(training, :) == -1);
    learner = svmtrain(ones(numel(y(training, :)), 1), y(training, :), x(training, :), sprintf(param, positive, negative));
    
    % compare the predictions on this new dimensional space
    predictions = svmpredict(y(testing, :), x(testing, :), learner);
    cv_accuracy(idx) = sum(predictions == y(testing, :)) / size(y(testing, :), 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
