clear; close all;

load('seeds.mat'); rng(s);

[labels_global, instances_global] = libsvmread('Data/n-gram.data');

to_plot = 'accuracy'; % or n_sv

S = 100; N = round(size(instances_global, 1) / S) + 1;
labels = []; instances = [];
accuracy_x = zeros(N + 1, 1); accuracy_y = zeros(N + 1, 1);
accuracy_x(1) = 0; accuracy_y(1) = 0;
n_sv_x = zeros(N + 1, 1); n_sv_y = zeros(N + 1, 1);
n_sv_x(1) = 0; n_sv_y(1) = 0;
params = '-t 0 -c 1 -h 0 -w1 %.3f -w-1 %.3f';
% while all samples not processed
for i = 1 : N
    fprintf('Iteration #%d/%d', i, N);
    
    % pick another 'S' random samples
    if size(instances_global, 1) >= S
        indices = randsample(size(instances_global, 1), S);
    else
        indices = (1: size(instances_global, 1))';
    end
    instances = [instances; instances_global(indices, :);]; %#ok<AGROW>
    labels = [labels; labels_global(indices, :);]; %#ok<AGROW>
    % remove them from the global data
    instances_global(indices, :) = []; labels_global(indices, :) = [];
    
    % measure the cross validation accuracy on data until now
    accuracy_total = 0; n_sv_total = 0;
    cv = cvpartition(labels, 'Kfold', 10);
    for j = 1 : cv.NumTestSets
        training = cv.training(j);
        testing = cv.test(j);
        x_training = instances(training, :); y_training = labels(training, :);
        x_testing = instances(testing, :); y_testing = labels(testing, :);
        
        % train the model
        w = ones(size(x_training, 1), 1);
        positive = size(y_training, 1) / sum(y_training == 1);
        negative = size(y_training, 1) / sum(y_training == -1);
        model = svmtrain(w, y_training, x_training, sprintf(params, positive, negative));
        
        % get predictions
        [predictions, ~, ~] = svmpredict(y_testing, x_testing, model);
        
        % get accuracy and number of support vectors
        accuracy_total = accuracy_total + 100 * sum(predictions == y_testing) / size(y_testing, 1);
        n_sv_total = n_sv_total + model.totalSV;
    end
    
    % get accuracy and number of support vectors
    accuracy_x(i + 1) = size(instances, 1);
    accuracy_y(i + 1) = accuracy_total / cv.NumTestSets;
    n_sv_x(i + 1) = size(instances, 1);
    n_sv_y(i + 1) = n_sv_total / cv.NumTestSets;
end

if strcmp(to_plot, 'accuracy') == 1
    plot(accuracy_x, accuracy_y, 'bd-');
    axis([0 size(instances, 1) 0 100]);
    legend('Accuracy'); xlabel('Number of instances'); ylabel('Accuracy (%)');
elseif strcmp(to_plot, 'n_sv') == 1
    plot(n_sv_x, n_sv_y, 'bd-');
    axis([0 size(instances, 1) 0 max(n_sv_y) + 1000]);
    legend('Number of Support Vectors'); xlabel('Number of instances'); ylabel('Number of Support Vectors');
end
