clear; close all;

[labels, instances] = libsvmread('Data/a1a.data');

% parameters
cv = cvpartition(labels, 'HoldOut', 0.5);
M = 9;
param = '-t 0 -c 1';

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
for m = 1 : M
    % train the model
    learners{m} = svmtrain(ones(2, 1), [y_training(i, :); y_training(j, :);], [x_training(i, :); x_training(j, :);], param);
    % store the support vectors
    sv_instances{m} = learners{m}.SVs;
    sv_labels{m} = svmpredict(ones(2, 1), sv_instances{m}, learners{m});
    % predict accuracy on the testing data
    [~, a, ~] = svmpredict(y_testing, x_testing, learners{m});
    accuracy(1) = a(1) / 100;
end
x_training(i, :) = []; y_training(i, :) = [];
x_training(j, :) = []; y_training(j, :) = [];

% continue for the rest of the samples
n = size(x_training, 1);
for i = 1 : n
    % retrain all the models
    for m = 1 : M
        x = [sv_instances{m}; x_training(i, :);];
        y = [sv_labels{m}; y_training(i, :);];
        w = ones(size(x, 1), 1);
        learners{m} = svmtrain(w, y, x, param);
        sv_instances{m} = learners{m}.SVs;
        sv_labels{m} = svmpredict(ones(size(sv_instances{m}, 1), 1), sv_instances{m}, learners{m});
    end
    % store the accuracy resulting after this sample
    predictions = zeros(size(y_testing, 1), M);
    for m = 1 : M
        predictions(:, m) = svmpredict(y_testing, x_testing, learners{m});
    end
    predictions = sign(sum(predictions, 2));
    accuracy(i + 1) = sum(predictions == y_testing) / size(y_testing, 1);
end

plot(accuracy);