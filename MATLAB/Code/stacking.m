[labels, instances] = libsvmread('Data/a1a.data');

n_global = size(instances, 1);

cv = 5;
cv_accuracy = zeros(1, cv);

type = 'svm';

for idx = 1 : cv
    fprintf('Iteration #%d\n', idx);
    
    testing = randsample(n_global, round(n_global/cv));
    training = setdiff((1:n_global), testing)';
    
    % input data for the first level learners
    x_training = instances(training, :); y_training = labels(training, :);
    
    % train individual learners on the training data (first level)
    if strcmp(type, 'svm') == 1
        n_c = 3; n_gamma = 3;
        c_all = linspace(1, 100, n_c);
        gamma_all = linspace(0, 1, n_gamma);
        learners = cell(n_c * n_gamma, 1);
        idx_learner = 1;
        for j = 1 : n_c
            for k = 1 : n_gamma
                param = sprintf('-t 2 -c %s -g %.3f -h 0 ', num2str(c_all(j)), gamma_all(k));
                learners{idx_learner} = weak_learner_train('stacking', x_training, y_training, 'svm', param);
                idx_learner = idx_learner + 1;
            end
        end
    elseif strcmp(type, 'tree') == 1
        n_l = 10;
        idx_learner = 1;
        learners = cell(n_l, 1);
        for j = 1 : n_l
            learners{idx_learner} = weak_learner_train('stacking', x_training, y_training, 'tree');
            idx_learner = idx_learner + 1;
        end
    end
    
    m = size(learners, 1);
    
    % prepare the data for the second level learner using the outputs from
    % the first level learners
    x = zeros(n_global, m);
    y = labels;
    for i = 1 : m
        x(:, i) = weak_learner_predict(instances, labels, learners{i}{1}, learners{i}{2});
    end
    
    % train the second level learner
    learner = weak_learner_train('stacking', x(training, :), y(training, :), 'tree');
    
    % test performance over the testing dataset
    predictions = weak_learner_predict(x(testing, :), y(testing, :), learner{1}, learner{2});
    cv_accuracy(idx) = sum(predictions == y(testing, :)) / size(y(testing, :), 1);
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy)));
