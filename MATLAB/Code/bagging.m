clear all;

[labels, instances] = libsvmread('Data/a1a.data');

cv = 5;
n_global = size(labels, 1);
cv_accuracy = zeros(1, cv);

for i = 1 : cv
    fprintf('Iteration #%d\n', i);
    
    % initialize training/testing dataset
    testing = randsample(n_global, round(n_global/cv));
    training = setdiff((1:n_global), testing)';
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    
    % build the weak learners
    learners = cell(3, 1);
    learners{1} = weak_learner_train('bagging', x_training, y_training, 'tree');
    learners{2} = weak_learner_train('bagging', x_training, y_training, 'tree');
    learners{3} = weak_learner_train('bagging', x_training, y_training, 'tree');

    % predict on the testing data
    predictions = bagging_predict(x_testing, learners);
    
    cv_accuracy(i) = sum(y_testing == predictions) / size(y_testing, 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
