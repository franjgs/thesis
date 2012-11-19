clear; close all;

[labels, instances] = libsvmread('Data/n-gram.data');

cv = cvpartition(labels, 'HoldOut', 0.5);
M = 10;

libsvm_accuracy = zeros(1, cv.NumTestSets);
boosting_accuracy = zeros(1, cv.NumTestSets);
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
    
    % boosting
    % ---------------------------------------------------------------------
    models = cell(M, 1);
    n = size(x_training, 1);
    w = repmat(1/n, n, M + 1);
    alpha = zeros(M, 1);
    eps = zeros(M, 1);
    % build the committee
    for m = 1 : M
        % eq. 14.15
        models{m} = svmtrain(w(:, m) ./ min(w(:, m)), y_training, x_training, params);
        [predictions, ~, ~] = svmpredict(y_training, x_training, models{m});
        I = (predictions ~= y_training);
        % eq. 14.16
        eps(m) = (w(:, m)' * I) / sum(w(:, m));
        % eq. 14.17
        alpha(m) = log((1 - eps(m)) / eps(m));
        % eq. 14.18
        w(:, m + 1) = w(:, m) .* exp(alpha(m) * I);
    end
    % test predictions on the testing data (eq. 14.19)
    predictions = zeros(size(y_testing, 1), M);
    for m = 1 : M
        [predictions(:, m), ~, ~] = svmpredict(y_testing, x_testing, models{m});
    end
    predictions = sign(predictions * alpha);
    boosting_accuracy(i) = sum(predictions == y_testing) / size(y_testing, 1);
    % ---------------------------------------------------------------------
end

fprintf('\n');
fprintf('libsvm accuracy => [%s]\nmean => %s\n', num2str(libsvm_accuracy), num2str(mean(libsvm_accuracy)));
fprintf('boosting accuracy => [%s]\nmean => %s\n', num2str(boosting_accuracy), num2str(mean(boosting_accuracy)));
