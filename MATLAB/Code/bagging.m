clear; close all;

[labels, instances] = libsvmread('Data/a1a.data');

M = 99;
cv = cvpartition(labels, 'HoldOut', 0.5);
cv_accuracy = zeros(1, cv.NumTestSets);

for i = 1 : cv.NumTestSets
    fprintf('Iteration #%d\n', i);
    
    % initialize training/testing dataset
    training = cv.training(i);
    testing = cv.test(i);
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    
    % build the weak learners
    n = size(x_training, 1);
    learners = cell(M, 1);
    for m = 1 : M
        indices = randsample(n, randi([round(n/2), n]));
        w = ones(size(indices, 1), 1);
        learners{m} = svmtrain(w, y_training(indices, :), x_training(indices, :), '-t 0 -c 1 -h 0');
    end

    % predict on the testing data
    n = size(x_testing, 1);
    predictions = zeros(n, M);
    for m = 1 : M
        [predictions(:, m), ~, ~] = svmpredict(y_testing, x_testing, learners{m});
    end
    predictions = sign(sum(predictions, 2));
    
    cv_accuracy(i) = sum(y_testing == predictions) / size(y_testing, 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
