% given the learners, and the feature indices these learners work on
% obtain predictions from all the learners, and take a weighted vote
function [labels] = random_subspace_predict(instances, learners, features, clf_accuracy)
    n = size(instances, 1);
    m = size(learners, 1);
    outputs = zeros(n, m);
    for i = 1 : m
        outputs(:, i) = weak_learner_predict(instances(:, features{i}), zeros(n, 1), learners{i}{1}, learners{i}{2});
    end
    labels = sign(outputs * clf_accuracy);
end
