clear; close all;

load('seeds.mat'); rng(s);

[labels_global, instances_global] = libsvmread('Data/n-gram.data');

S = 100; N = round(size(instances_global, 1) / S) + 1; M = 9;
labels = []; instances = [];
accuracy_x = zeros(N + 1, 1); accuracy_y = zeros(N + 1, 1);
accuracy_x(1) = 0; accuracy_y(1) = 0;
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
    accuracy_total = 0;
    cv = cvpartition(labels, 'Kfold', 10);
    for j = 1 : cv.NumTestSets
        training = cv.training(j);
        testing = cv.test(j);
        x_training = instances(training, :); y_training = labels(training, :);
        x_testing = instances(testing, :); y_testing = labels(testing, :);
        
        % train the models (first and second level)
        n = size(x_training, 1);
        models = cell(M, 1);
        for m = 1 : M
            indices = randsample(n, randi([round(n/2), n]));
            w = ones(size(indices, 1), 1);
            positive = numel(indices) / sum(y_training(indices, :) == 1);
            negative = numel(indices) / sum(y_training(indices, :) == -1);
            models{m} = svmtrain(w, y_training(indices, :), x_training(indices, :), sprintf(params, positive, negative));
        end
        x = zeros(n, M); y = y_training;
        for m = 1 : M
            [x(:, m), ~, ~] = svmpredict(y_training, x_training, models{m});
        end
        w = ones(size(x, 1), 1);
        positive = size(y, 1) / sum(y == 1);
        negative = size(y, 1) / sum(y == -1);
        model = svmtrain(w, y, x, sprintf(params, positive, negative));
    
        % get predictions
        n = size(x_testing, 1); w = ones(n, 1);
        x = zeros(n, M); y = y_testing;
        for m = 1 : M
            [x(:, m), ~, ~] = svmpredict(y_testing, x_testing, models{m});
        end
        [predictions, ~, ~] = svmpredict(y, x, model);
        
        % get accuracy
        accuracy_total = accuracy_total + 100 * sum(predictions == y_testing) / size(y_testing, 1);
    end
    
    % get accuracy
    accuracy_x(i + 1) = size(instances, 1);
    accuracy_y(i + 1) = accuracy_total / cv.NumTestSets;
end

plot(accuracy_x, accuracy_y, 'bd-');
axis([0 size(instances, 1) 0 100]);
legend('Accuracy'); xlabel('Number of instances'); ylabel('Accuracy (%)');
