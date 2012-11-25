clear; close all;

load('seeds.mat'); rng(s);

[labels, instances] = libsvmread('Data/a1a.data');

n_global = size(instances, 1);

cv = 5;
cv_accuracy = zeros(1, cv);

features_per_learner = 10;
num_features = size(instances, 2);
num_learners = round(num_features / features_per_learner);
param = '-t 0 -c 1 -h 0 -w1 %.3f -w-1 %.3f';

for idx = 1 : cv
    fprintf('Iteration %d\n', idx);
    
    testing = randsample(n_global, round(n_global/cv));
    training = setdiff((1: n_global), testing)';
    
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    
    % build the weak learners
    fprintf('Training %d learners...', num_learners);
    learners = cell(num_learners, 1);
    for i = 1 : num_learners
        start = ((i - 1) * features_per_learner) + 1;
        finish = i * features_per_learner;
        if finish > num_features
            finish = num_features;
        end
        positive = size(y_training, 1) / sum(y_training == 1);
        negative = size(y_training, 1) / sum(y_training == -1);
        learners{i} = svmtrain(ones(size(y_training, 1), 1), y_training, x_training(:, start: finish), sprintf(param, positive, negative));
    end
    fprintf('Done\n');
    
    % transform the dataset into n*m matrix
    fprintf('Transforming the dataset into the new feature space...');
    x = zeros(n_global, num_learners);
    y = labels;
    for i = 1 : num_learners
        start = ((i - 1) * features_per_learner) + 1;
        finish = i * features_per_learner;
        if finish > num_features
            finish = num_features;
        end
        x(:, i) = svmpredict(labels, instances(:, start: finish), learners{i});
    end
    fprintf('Done\n');
    
    positive = numel(y(training, :)) / sum(y(training, :) == 1);
    negative = numel(y(training, :)) / sum(y(training, :) == -1);
    learner = svmtrain(ones(size(training, 1), 1), y(training, :), x(training, :), sprintf(param, positive, negative));
    
    predictions = svmpredict(y(testing, :), x(testing, :), learner);
    
    cv_accuracy(idx) = sum(predictions == y(testing, :)) / size(y(testing, :), 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
