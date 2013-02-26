clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/n-gram.data');

cv = cvpartition(labels, 'HoldOut', 0.3);
cv_accuracy = zeros(1, cv.NumTestSets);
param = '-t 0 -c 1 -h 0 -w1 %.3f -w-1 %.3f';

for i = 1 : cv.NumTestSets
    fprintf('Iteration #%d\n', i);
    
    % initialize training/testing dataset
    training = cv.training(i);
    testing = cv.test(i);
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    
    % train the model
    n = size(x_training, 1);
    w = ones(size(x_training, 1), 1);
    positive = size(y_training, 1) / sum(y_training == 1);
    negative = size(y_training, 1) / sum(y_training == -1);
    param = sprintf('-t 0 -c %s -w1 %.3f -w-1 %.3f', num2str(i * 10), positive, negative);
    model = svmtrain(w, y_training, x_training, param);

    % predict on the testing data
    [predictions, ~, ~] = svmpredict(y_testing, x_testing, model);
    
    cv_accuracy(i) = sum(y_testing == predictions) / size(y_testing, 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
