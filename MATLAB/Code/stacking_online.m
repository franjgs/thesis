clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/a1a.data');

cv = cvpartition(labels, 'HoldOut', 0.5);
M = 8;
param = '-t 0 -c 1 -w1 %.3f -w-1 %.3f';

% define training/testing data
training = cv.training(1);
testing = cv.test(1);
x_training = instances(training, :); y_training = labels(training, :);
x_testing = instances(testing, :); y_testing = labels(testing, :);

% accuracy to be plotted
accuracy = zeros(1, size(x_training, 1));

% train learners for the first two (separable) samples
learners = cell(M, 1);
sv_instances = cell(M, 1);
sv_labels = cell(M, 1);
i = find(y_training == 1, 1);
j = find(y_training == -1, 1);
n_testing = size(y_testing, 1);
x = zeros(n_testing, M);
y = y_testing;
for m = 1 : M
    % train the learners
    positive = 0.5; negative = 0.5;
    learners{m} = svmtrain(ones(2, 1), [y_training(i, :); y_training(j, :);], [x_training(i, :); x_training(j, :);], sprintf(param, positive, negative));
    % update support vectors
    sv_instances{m} = learners{m}.SVs;
    sv_labels{m} = svmpredict(ones(size(sv_instances{m}, 1), 1), sv_instances{m}, learners{m});
    % convert the testing data to the new dimensional space
    x(:, m) = svmpredict(y_testing, x_testing, learners{m});
end
positive = size(y, 1) / sum(y == 1);
negative = size(y, 1) / sum(y == -1);
learner = svmtrain(ones(n_testing, 1), y, x, sprintf(param, positive, negative));
predictions = svmpredict(y, x, learner);
accuracy(1) = sum(predictions == y) / size(y, 1);
x_training(i, :) = []; y_training(i, :) = [];
x_training(j, :) = []; y_training(j, :) = [];

% continue with the rest of the samples
N = size(x_training, 1);
for n = 1 : N
    x = zeros(n_testing, M); y = y_testing;
    for m = 1 : M
        % train the models
        w = ones(size(sv_instances{m}, 1) + 1, 1);
        x_now = [sv_instances{m}; x_training(i, :);];
        y_now = [sv_labels{m}; y_training(i, :);];
        positive = size(y_now, 1) / sum(y_now == 1);
        negative = size(y_now, 1) / sum(y_now == -1);
        learners{m} = svmtrain(w, y_now, x_now, sprintf(param, positive, negative));
        % pick new support vectors
        sv_instances{m} = learners{m}.SVs;
        sv_labels{m} = svmpredict(ones(size(sv_instances{m}, 1), 1), sv_instances{m}, learners{m});
        % prepare data for higher dimensional space
        x(:, m) = svmpredict(y_testing, x_testing, learners{m});
    end
    positive = size(y, 1) / sum(y == 1);
    negative = size(y, 1) / sum(y == -1);
    learner = svmtrain(ones(n_testing, 1), y, x, sprintf(param, positive, negative));
    predictions = svmpredict(y, x, learner);
    accuracy(i + 1) = sum(predictions == y) / size(y, 1);
end

plot(accuracy);
