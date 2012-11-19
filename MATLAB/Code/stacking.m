clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/a1a.data');

n_global = size(instances, 1);

cv = cvpartition(labels, 'HoldOut', 0.5);
cv_accuracy = zeros(1, cv.NumTestSets);

M = 10;

for idx = 1 : cv.NumTestSets
    fprintf('Iteration #%d\n', idx);
    
    training = cv.training(idx);
    testing = cv.test(idx);
    
    % input data for the first level learners
    x_training = instances(training, :); y_training = labels(training, :);
    
    % train individual learners on the training data (first level)
    learners = cell(M, 1);
    idx_learner = 1;
    w = ones(size(x_training, 1), 1);
    positive = size(y_training, 1) / sum(y_training == 1);
    negative = size(y_training, 1) / sum(y_training == -1);
    for i = 1 : M
        param = sprintf('-t 0 -c %s -w1 %.3f -w-1 %.3f', num2str(i * 10), positive, negative);
        learners{idx_learner} = svmtrain(w, y_training, x_training, param);
        idx_learner = idx_learner + 1;
    end
    
    m = size(learners, 1);
    
    % prepare the data for the second level learner using the outputs from
    % the first level learners
    x = zeros(n_global, m);
    y = labels;
    for i = 1 : m
        x(:, i) = svmpredict(labels, instances, learners{i});
    end
    
    % train the second level learner
    learner = svmtrain(w, y(training, :), x(training, :), '-t 0 -c 1');
    
    % test performance over the testing dataset
    predictions = svmpredict(y(testing, :), x(testing, :), learner);
    cv_accuracy(idx) = sum(predictions == y(testing, :)) / size(y(testing, :), 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
