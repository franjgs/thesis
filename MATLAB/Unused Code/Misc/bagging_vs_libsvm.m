clear; close all;

[labels, instances] = libsvmread('Data/a1a.data');

cv = cvpartition(labels, 'KFold', 5);
M = 9;

libsvm_accuracy = zeros(1, cv.NumTestSets);
bagging_accuracy = zeros(1, cv.NumTestSets);
for i = 1 : cv.NumTestSets
    training = cv.training(i);
    testing = cv.test(i);
    
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    positive = sum(y_training == 1) / size(y_training, 1);
    negative = sum(y_training == -1) / size(y_training, 1);
    params = sprintf('-t 0 -c 1 -w1 %.3f -w-1 %.3f', positive, negative);
    
    % libsvm
    % ---------------------------------------------------------------------
    w = ones(size(y_training, 1), 1);
    model = svmtrain(w, y_training, x_training, params);
    [p, a, d] = svmpredict(y_testing, x_testing, model);
    libsvm_accuracy(i) = a(1) / 100;
    % ---------------------------------------------------------------------
    
    % bagging
    % ---------------------------------------------------------------------
    models = cell(M, 1);
    n = size(x_training, 1);
    predictions = zeros(size(y_testing, 1), M);
    for j = 1 : M
        indices = randsample(n, randi([round(n/2), n]));
        w = ones(size(indices, 1), 1);
        models{j} = svmtrain(w, y_training(indices, :), x_training(indices, :), params);
        [predictions(:, j), ~, ~] = svmpredict(y_testing, x_testing, models{j});
    end
    predictions = sign(sum(predictions, 2));
    bagging_accuracy(i) = sum(predictions == y_testing) / size(y_testing, 1);
    % ---------------------------------------------------------------------
end

fprintf('\n');
fprintf('libsvm accuracy => [%s]\nmean => %s\n', num2str(libsvm_accuracy), num2str(mean(libsvm_accuracy)));
fprintf('bagging accuracy => [%s]\nmean => %s\n', num2str(bagging_accuracy), num2str(mean(bagging_accuracy)));
