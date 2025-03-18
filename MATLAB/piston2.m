l_c = 30;
l_s = 100;
timestep = 0.01;

time = 0:timestep:4;
y = l_c*cos(time*10) + l_s;

ydot = zeros(size(time));
for i = 2:length(time)
    ydot(i) = (y(i) - y(i-1)) / timestep;
end

th = arrayfun(@(y, ydot) crank_pos(y,ydot,l_c,l_s), y, ydot);

function th = crank_pos(y, ydot, l_c, l_s)
    th = acos((y^2 + l_c^2 - l_s^2) / (2*y*l_c));
    if ydot > 0 %Correct arccos domain
        th = -th;
    end
end