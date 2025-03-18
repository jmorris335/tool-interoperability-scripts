l_c = 30;
l_s = 100;
timestep = 0.01;

time = 0:timestep:4;
omega = 2*pi;

theta = zeros(size(time));
for i = 2:length(time)
    theta(i) = theta(i-1) + omega * timestep;
end

y = arrayfun(@(th) piston_height(th,l_c,l_s), theta);

function y = piston_height(th, l_c, l_s)
    y = l_c * cos(th) + sqrt(l_s^2 - l_c^2 * sin(th)^2);
end