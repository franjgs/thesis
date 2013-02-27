clear; close all;

load('seeds.mat'); rng(s);

[labels_global, instances_global] = libsvmread('Data/n-gram.data');

labels = []; instances = []; S = 100; N = round(size(instances_global, 1) / S);
accuracy = zeros(N, 1); M = 9;
params = '-t 0 -c 1 -h 0 -w1 %.3f -w-1 %.3f';
% while all samples not processed
for i = 1 : N
    fprintf('Iteration #%d/%d', i, N);
    
    % pick another 'S' random samples
    if size(instances_global, 1) >= S
        indices = randsample(size(instances_global, 1), S);
    else
        indices = (1: size(instances_global, 1))';
    end
    instances = [instances; instances_global(indices, :);]; %#ok<AGROW>
    labels = [labels; labels_global(indices, :);]; %#ok<AGROW>
    % remove them from the global data
    instances_global(indices, :) = []; labels_global(indices, :) = [];
    
    % measure the cross validation accuracy on data until now
    cv = cvpartition(labels, 'HoldOut', 0.3);
    training = cv.training(1);
    testing = cv.test(1);
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    
    % train the 'M' models
    n = size(x_training, 1);
    learners = cell(M, 1);
    for m = 1 : M
        indices = randsample(n, randi([round(n/2), n]));
        w = ones(size(indices, 1), 1);
        positive = numel(indices) / sum(y_training(indices, :) == 1);
        negative = numel(indices) / sum(y_training(indices, :) == -1);
        learners{m} = svmtrain(w, y_training(indices, :), x_training(indices, :), sprintf(params, positive, negative));
    end
    
    % predict on the testing data
    n = size(x_testing, 1);
    predictions = zeros(n, M);
    for m = 1 : M
        [predictions(:, m), ~, ~] = svmpredict(y_testing, x_testing, learners{m});
    end
    predictions = sign(sum(predictions, 2));
    
    % get accuracy
    accuracy(i) = sum(predictions == y_testing) / size(y_testing, 1);
end

plot(accuracy);
