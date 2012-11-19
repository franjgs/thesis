clear all;

[labels, instances] = libsvmread('Data/a1a.data');

cv = cvpartition(labels, 'HoldOut', 0.5);
cv_accuracy = zeros(1, cv.NumTestSets);

for i = 1 : cv.NumTestSets;
    training = cv.training(i);
    testing = cv.test(i);
    
    x_training = instances(training, :); y_training = labels(training, :);
    x_testing = instances(testing, :); y_testing = labels(testing, :);
    
    positive = sum(y_training == 1) / size(y_training, 1);
    negative = sum(y_training == -1) / size(y_training, 1);
    w = ones(size(x_training, 1), 1);
    
    model = svmtrain(w, y_training, x_training, sprintf('-t 0 -c 1 -w1 %.3f -w-1 %.3f', positive, negative));
    
    [p, a, d] = svmpredict(y_testing, x_testing, model);
    
    cv_accuracy(i) = a(1) / 100;
end

fprintf('Accuracy => [%s]\nMean => %s\n', num2str(cv_accuracy), num2str(mean(cv_accuracy) * 100));
