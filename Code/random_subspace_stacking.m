clear all;

[labels, instances] = libsvmread('Data/a1a.data');

n_global = size(instances, 1);
cv = 5;
cv_accuracy = zeros(1, cv);

features_per_learner = 10;
num_features = size(instances, 2);
num_learners = round(num_features / features_per_learner);

for idx = 1 : cv
    fprintf('Iteration #%d\n', idx);
    
    testing = randsample(n_global, round(n_global/cv));
    training = setdiff((1: n_global), testing)';
    
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    
    fprintf('Training %d learners...', num_learners);
    learners = cell(num_learners, 1);
    features = cell(num_learners, 1);
    for i = 1 : num_learners
        % pick out random features
        if size(x_training, 2) < features_per_learner
            feature_indices = (1: size(x_training, 2))';
        else
            feature_indices = randsample(size(x_training, 2), features_per_learner);
        end
        features{i} = feature_indices;
        % train the learners on these features
        learners{i} = weak_learner_train('random_subspace', x_training(:, features{i}), y_training, 'tree');
        % remove the features from the training data
        x_training(:, feature_indices) = [];
    end
    fprintf('Done\n');
    
    % transform the data into the new dimensional space
    x = zeros(n_global, num_learners);
    y = labels;
    for i = 1 : num_learners
        x(:, i) = weak_learner_predict(instances(:, features{i}), labels, learners{i}{1}, learners{i}{2});
    end
    
    % train a new learner on this new dimensional space
    learner = weak_learner_train('random_subspace_stacking', x(training, :), y(training, :), 'tree');
    
    % compare the predictions on this new dimensional space
    predictions = weak_learner_predict(x(testing, :), y(testing, :), learner{1}, learner{2});
    cv_accuracy(idx) = sum(predictions == y(testing, :)) / size(y(testing, :), 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
