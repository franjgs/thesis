function output = boosting_predict(instances, models, alpha)
    n = size(instances, 1);
    m = size(models, 1);
    labels = zeros(n, m);
    % predict labels from all models, multiply each prediction by its
    % corresponding alpha, take the row wise sum, and take the sign
    for idx = 1 : m
        labels(:, idx) = weak_learner_predict(instances, zeros(n, 1), models{idx}{1}, models{idx}{2});
    end
    output = sign(labels * alpha);
end