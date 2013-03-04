% total number of samples for each class
n = 200;

radius = 10;
theta = 2 * pi * rand(n, 1);

% points inside the circle
r_in = rand(n, 1) * radius;
x_in = r_in .* cos(theta);
y_in = r_in .* sin(theta);
label_in = ones(n, 1);

% points outside the circle
r_out = radius + rand(n, 1) * radius;
x_out = r_out .* cos(theta);
y_out = r_out .* sin(theta);
label_out = -1 * ones(n, 1);

instances = [x_in y_in; x_out y_out;];
labels = [label_in; label_out;];
