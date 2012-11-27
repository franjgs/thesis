function [output] = bagging_predict(instances, learners)
    n = size(instances, 1);
    m = size(learners, 1);
    output = zeros(n, 1);
    for i = 1 : m
        output(:, i) = weak_learner_predict(instances, zeros(n, 1), learners{i}{1}, learners{i}{2});
    end
    output = sign(sum(output, 2));
end
