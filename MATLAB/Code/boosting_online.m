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
    
        % train the 'M' models
        models = cell(M, 1);
        n = size(x_training, 1);
        m_max = 1;
        w = repmat(1 / n, n, M);
        alpha = zeros(M, 1);
        eps = zeros(M, 1);
        for m = 1 : M
            m_max = m;
            positive = size(y_training, 1) / sum(y_training == 1);
            negative = size(y_training, 1) / sum(y_training == -1);
            models{m} = svmtrain(w(:, m) ./ min(w(:, m)), y_training, x_training, sprintf(params, positive, negative));
            predictions = svmpredict(y_training, x_training, models{m});
            I = (predictions ~= y_training);
            if sum(I) == 0
                eps(m) = 0;
                alpha(m) = max(alpha) + 1;
                break;
            else
                eps(m) = (w(:, m)' * I) / sum(w(:, m));
                alpha(m) = log ( (1 - eps(m)) / eps(m) );
            end
            if m < M
                w(:, m + 1) = w(:, m) .* exp(alpha(m) * I);
            end
        end
    
        % predict on the testing data
        predictions = zeros(size(x_testing, 1), M);
        for m = 1 : m_max
            [predictions(:, m), ~, ~] = svmpredict(y_testing, x_testing, models{m});
        end
        predictions = sign(predictions * alpha);
        
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
