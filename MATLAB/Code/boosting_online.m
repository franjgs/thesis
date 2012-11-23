clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/a1a.data');
labels = labels(1: 100, :);
instances = instances(1: 100, :);

% parameters
cv = cvpartition(labels, 'HoldOut', 0.5);
M = 8;
param = '-t 0 -c %d -w1 %.3f -w-1 %.3f';

% define training/testing data
training = cv.training(1);
testing = cv.test(1);
x_training = instances(training, :); y_training = labels(training, :);
x_testing = instances(testing, :); y_testing = labels(testing, :);

% data to be plotted
accuracy = zeros(1, size(x_training, 1) - 1);

% store learners and support vectors for each of the M models
learners = cell(M, 1);
sv_instances = cell(M, 1);
sv_labels = cell(M, 1);

% find two training instances with labels 1 and -1
i = find(y_training == 1, 1);
j = find(y_training == -1, 1);
predictions = zeros(size(y_testing, 1), M);
for m = 1 : M
    % train the model
    positive = 0.5; negative = 0.5;
    learners{m} = svmtrain(ones(2, 1), [y_training(i, :); y_training(j, :);], [x_training(i, :); x_training(j, :);], sprintf(param, m, positive, negative));
    % store the support vectors
    sv_instances{m} = learners{m}.SVs;
    sv_labels{m} = svmpredict(ones(2, 1), sv_instances{m}, learners{m});
    % calculate predictions on testing data
    predictions(:, m) = svmpredict(y_testing, x_testing, learners{m});
end
predictions = sign(sum(predictions, 2));
accuracy(1) = sum(predictions == y_testing) / size(y_testing, 1);
x_training(i, :) = []; y_training(i, :) = [];
x_training(j, :) = []; y_training(j, :) = [];

% continue for the rest of the samples
N = size(x_training, 1);
for i = 1 : N
    % first, retrain the models
    n = size(sv_instances{m}, 1) + 1;
    w = repmat(1 / n, n, M);
    alpha = zeros(M, 1);
    eps = zeros(M, 1);
    for m = 1 : M
        % TODO: Handle the case where I is an all-zero matrix, which
        % results in a zero epsilon and infinite alpha
        x = [sv_instances{m}; x_training(i, :);];
        y = [sv_labels{m}; y_training(i, :);];
        positive = size(y, 1) / sum(y == 1);
        negative = size(y, 1) / sum(y == -1);
        learners{m} = svmtrain(w(:, m) ./ min(w(:, m)), y, x, sprintf(param, m, positive, negative));
        predictions = svmpredict(y, x, learners{m});
        I = (predictions ~= y);
        eps(m) = (w(:, m)' * I) / sum(w(:, m));
        alpha(m) = log ( (1 - eps(m)) / eps(m) );
        if m < M
            w(:, m + 1) = w(:, m) .* exp(alpha(m) * I);
        end
        sv_instances{m} = learners{m}.SVs;
        sv_labels{m} = svmpredict(ones(size(sv_instances{m}, 1), 1), sv_instances{m}, learners{m});
    end
    % measure the accuracy resulting from this model
    predictions = zeros(size(y_testing, 1), M);
    for m = 1 : M
        predictions(:, m) = svmpredict(y_testing, x_testing, learners{m});
    end
    predictions = sign(predictions * alpha);
    accuracy(i + 1) = sum(predictions == y_testing) / size(y_testing, 1);
end

plot(accuracy);
