clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/n-gram.data');

M = 50;
accuracy_x = zeros(M + 1, 1); accuracy_y = zeros(M + 1, 1);
accuracy_x(1) = 0; accuracy_y(1) = 0;
params = '-t 0 -c 1 -h 0 -w1 %.3f -w-1 %.3f';
for m = 1 : M
    fprintf('Number of models %d/%d', m, M);

    % divide the data into training/testing halves
    cv = cvpartition(labels, 'HoldOut', 0.3);
    training = cv.training(1);
    testing = cv.test(1);
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);

    % train the 'm' models
    n = size(x_training, 1);
    learners = cell(m, 1);
    for i = 1 : m
        indices = randsample(n, randi([round(n/2), n]));
        w = ones(size(indices, 1), 1);
        positive = numel(indices) / sum(y_training(indices, :) == 1);
        negative = numel(indices) / sum(y_training(indices, :) == -1);
        learners{i} = svmtrain(w, y_training(indices, :), x_training(indices, :), sprintf(params, positive, negative));
    end

    % predict on the testing data
    n = size(x_testing, 1);
    predictions = zeros(n, m);
    for i = 1 : m
        [predictions(:, i), ~, ~] = svmpredict(y_testing, x_testing, learners{i});
    end
    predictions = sign(sum(predictions, 2));

    % get accuracy numbers
    accuracy_x(m + 1) = m;
    accuracy_y(m + 1) = 100 * sum(predictions == y_testing) / size(y_testing, 1);
end

plot(accuracy_x, accuracy_y, 'bd-');
axis([0 M 0 100]);
legend('Accuracy'); xlabel('Number of models'); ylabel('Accuracy (%)');
