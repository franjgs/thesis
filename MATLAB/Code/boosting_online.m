clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/n-gram.data');

cv = cvpartition(labels, 'HoldOut', 0.5);
M = 10;
alpha = zeros(M, 1);
eps = zeros(M, 1);
learners = cell(M, 1);
param = '-t 0 -c 1 -w1 %.3f -w-1 %.3f';

training = cv.training(1);
testing = cv.test(1);

x_training = instances(training, :); y_training = labels(training, :);
x_testing = instances(testing, :); y_testing = labels(testing, :);

accuracy = zeros(1, size(x_training, 1) - 1);
n_testing = size(x_testing, 1);

% find two samples with labels 1 and -1, as a starting point to the process
i = find(y_training == 1, 1);
j = find(y_training == -1, 1);
x = [x_training(i, :); x_training(j, :);];
y = [y_training(i, :); y_training(j, :);];
n = size(x, 1);
w = repmat(1 / n, n, M);
M_max = M;
buffer_x = x; buffer_y = y;
for m = 1 : M
    positive = 0.5; negative = 0.5;
    learners{m} = svmtrain(w, y, x, sprintf(param, positive, negative));
    predictions = svmpredict(y, x, learners{m});
    I = (predictions ~= y);
    if all(I == 0)
        eps(m) = 0.26; % 1 / (1 + e)
        alpha(m) = 1;
        M_max = m;
        break;
    end
    eps(m) = (w(:, m)' * I) / sum(w(:, m));
    alpha(m) = log ( (1 - eps(m)) / eps(m) );
    if m < M
        w(:, m + 1) = w(:, m) .* exp(alpha(m) * I);
    end
end
x_training(i, :) = []; y_training(i, :) = [];
x_training(j, :) = []; y_training(j, :) = [];
predictions = zeros(n_testing, M);
for m = 1 : M_max
    predictions(:, m) = svmpredict(y_testing, x_testing, learners{m});
end
predictions = sign(predictions * alpha);
accuracy(1) = sum(predictions == y_testing) / size(y_testing, 1);

% continue for the rest of the samples
N = size(x_training, 1);
for i = 1 : N
    % initialize constants used for this iteration
    x = [buffer_x; x_training(i, :);];
    y = [buffer_y; y_training(i, :);];
    n = size(x, 1);
    w = repmat(1/n, n, M);
    positive = size(y, 1) / sum(y == 1);
    negative = size(y, 1) / sum(y == -1);
    M_max = M;
    % train all the models
    for m = 1 : M
        learners{m} = svmtrain(w(:, m) ./ min(w(:, m)), y, x, sprintf(param, positive, negative));
        predictions = svmpredict(y, x, learners{m});
        I = (predictions ~= y);
        if all(I == 0)
            eps(m) = 0.26;
            alpha(m) = 1;
            M_max = m;
            break
        end
        eps(m) = (w(:, m)' * I) / sum(w(:, m));
        alpha(m) = log ( (1 - eps(m)) / eps(m) );
        if m < M
            w(:, m + 1) = w(:, m) .* exp(alpha(m) * I);
        end
    end
    % measure accuracy on testing data
    predictions = zeros(n_testing, M);
    for m = 1 : M_max
        predictions(:, m) = svmpredict(y_testing, x_testing, learners{m});
    end
    predictions = sign(predictions * alpha);
    accuracy(i + 1) = sum(predictions == y_testing) / size(y_testing, 1);
    % update the instances in the buffer (pick the support vectors from the
    % last model)
    buffer_x = learners{M_max}.SVs;
    buffer_y = svmpredict(ones(size(buffer_x, 1), 1), buffer_x, learners{M_max});
end

plot(accuracy);
