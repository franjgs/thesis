clear; close all;

[labels, instances] = libsvmread('Data/a1a.data');

cv = cvpartition(labels, 'HoldOut', 0.5);

levels = 5;
M = 10;

libsvm_accuracy = zeros(1, cv.NumTestSets);
stacking_accuracy = zeros(1, cv.NumTestSets);

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
    
    % stacking
    % ---------------------------------------------------------------------
    n = size(instances, 1);
    w = ones(n, 1);
    x = instances; y = labels;
    for j = 1 : levels
        models = cell(M, 1);
        x_next = zeros(n, M);
        for m = 1 : M
            models{m} = svmtrain(w(training, :), y(training, :), x(training, :), params);
            [x_next(:, m), ~, ~] = svmpredict(y, x, models{m});
        end
        x = x_next;
    end
    model = svmtrain(w(training, :), y(training, :), x(training, :), params);
    [predictions, ~, ~] = svmpredict(y(testing, :), x(testing, :), model);
    stacking_accuracy(i) = sum(predictions == y(testing, :)) / size(y(testing, :), 1);
    % ---------------------------------------------------------------------
end

fprintf('\n');
fprintf('libsvm accuracy => [%s]\nmean => %s\n', num2str(libsvm_accuracy), num2str(mean(libsvm_accuracy)));
fprintf('stacking accuracy => [%s]\nmean => %s\n', num2str(stacking_accuracy), num2str(mean(stacking_accuracy)));
