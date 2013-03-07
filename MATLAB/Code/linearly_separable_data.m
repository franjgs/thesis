% generate data
n1 = 100; n2 = 100;
S1 = eye(2); S2 = eye(2);
m1 = [3; 0]; m2 = [-2; 0];
x1 = bsxfun(@plus, chol(S1)'*randn(2,n1), m1);
x2 = bsxfun(@plus, chol(S2)'*randn(2,n2), m2);
x = [x1 x2]'; y = [-ones(1,n1) ones(1,n2)]';

% plot
scatter(x(1:100, 1), x(1:100, 2), 'r');
hold on;
scatter(x(101:200, 1), x(101:200, 2), 'b');
hold off;
