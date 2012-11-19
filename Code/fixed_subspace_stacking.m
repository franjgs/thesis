clear all;

[labels, instances] = libsvmread('Data/a1a.data');

n_global = size(instances, 1);

cv = 5;
cv_accuracy = zeros(1, cv);

features_per_learner = 10;
num_features = size(instances, 2);
num_learners = round(num_features / features_per_learner);

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
        learners{i} = weak_learner_train('dimension_split', x_training(:, start: finish), y_training(:), 'tree');
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
        x(:, i) = weak_learner_predict(instances(:, start: finish), labels, learners{i}{1}, learners{i}{2});
    end
    fprintf('Done\n');
    
    learner = weak_learner_train('boosting', x(training, :), y(training, :), 'tree');
    
    predictions = weak_learner_predict(x(testing, :), y(testing, :), learner{1}, learner{2});
    
    cv_accuracy(idx) = sum(predictions == y(testing, :)) / size(y(testing, :), 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
