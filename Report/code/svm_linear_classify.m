% constants
n = 200; radius = 10; theta = 2 * pi * rand(n, 1);
    
% points inside the circle
r_in = rand(n, 1) * radius;
x_in = r_in .* cos(theta); y_in = r_in .* sin(theta);
label_in = ones(n, 1);
    
% points outside the circle
r_out = radius + rand(n, 1) * radius;
x_out = r_out .* cos(theta); y_out = r_out .* sin(theta);
label_out = -1 * ones(n, 1);

% final points
instances = [x_in y_in; x_out y_out;];
labels = [label_in; label_out;];

% plot the points in 2D
figure(1);
scatter(instances(1:200, 1), instances(1:200, 2), 'r');
hold on;
scatter(instances(201:400, 1), instances(201:400, 2), 'b');
hold off;

% transform the input to 3D and plot again
figure(2);
instances = [instances sqrt(power(instances(:, 1), 2) + power(instances(:, 2), 2))];
scatter3(instances(1:n, 1), instances(1:n, 2), instances(1:n, 3), 'r');
hold on;
scatter3(instances(n + 1:end, 1), instances(n + 1:end, 2), instances(n + 1:end, 3), 'b');
xlabel('X Axis'); ylabel('Y Axis'); zlabel('Z Axis'); grid on;
hold off;
