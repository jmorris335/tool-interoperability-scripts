function [] = animatePiston(time, y, th, C, step)
    persistent crank slider bob
    hold on

    crank = plot([0, C*cos(th(1))], [0, C*sin(th(1))], 'k-', 'LineWidth', 2);
    slider = plot([y(1), C*cos(th(1))], [0, y(1) - C*sin(th(1))], 'k-', 'LineWidth', 2);
    bob = plot(0, y(1), 'r.', 'MarkerSize', 20);

    gap = C/10;
    axis('equal')
    axis([-C - gap, C + gap, -C - gap, max(y) + gap])
    
    for i = 2:length(time)
        crank = drawCrank(crank, th(i), C);
        slider = drawSlider(slider, th(i), y(i), C);
        bob.YData = y(i);
        drawnow
        pause(step);
    end

end

function [crank] = drawCrank(crank, th, C)
    crank.XData = [0, C * sin(th)];
    crank.YData = [0, C * cos(th)];
end

function [slider] = drawSlider(slider, th, y, C)
    slider.XData = [0, C * sin(th)];
    slider.YData = [y, C * cos(th)];
end