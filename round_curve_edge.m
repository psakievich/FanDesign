clear; clc

c = 1000;   % desired chord length
m = 0.06;   % maximum camber
p = 0.50;   % fraction of chord where the maximum camber is located
t = 0.12;   % fraction of chord for thickness
r = 0.95;   % fraction of chord that is kept. Anything after r*c is rounded.

numtotalpts = 101;  % must be odd number..
numpoints = (numtotalpts+1)/2;

% First part of the camber line. (x<=pc)
yc_1 = @(x) m*x/p^2 .* (2*p - x/c);
% Second part of the camber line. (x>pc)
yc_2 = @(x) m*(c-x)/(1-p)^2 .* (1 + x/c - 2*p);

% Derivative for angle calculation.
d_yc_1 = @(x) (2*m/p^2) * (p-x/c);
d_yc_2 = @(x) (2*m/(1-p)^2) * (p-x/c);

% Thickness profile. y_t is 0.5 the thickness of the airfoil. For a
% symmetrical airfoil +y_t is the upper part of the airfoil, and -y_t is
% the lower part of the airfoil.
y_t = @(x) 5*t*c * (0.2969*sqrt(x/c) + (-0.1260)*(x/c) + (-0.3516)*(x/c).^2 + 0.2843*(x/c).^3 + (-0.1036)*(x/c).^4);

% Grid. Using somewhat chebyshev nodes for best resolution at leading and
% trailing edges.
x = zeros(numpoints,1);
a = 0; b = r*c + y_t(r*c);
for k = 1:numpoints;
  x(k) = 0.5*(a+b) + 0.5*(b-a)*cos( (k-1)/(numpoints-1) * pi);
end

x_l = zeros(numpoints,1);
y_l = zeros(numpoints,1);
x_u = zeros(numpoints,1);
y_u = zeros(numpoints,1);
for i = 1:numpoints;
  if( 0.0 <= x(i) && x(i) <= p*c )
    % front of airfoil
    theta = atan(d_yc_1(x(i)));
    x_u(i) = x(i) - y_t(x(i)) * sin(theta);
    y_u(i) = yc_1(x(i)) + y_t(x(i)) * cos(theta);
    
    x_l(i) = x(i) + y_t(x(i)) * sin(theta);
    y_l(i) = yc_1(x(i)) - y_t(x(i)) * cos(theta);
  elseif ( p*c < x(i) && x(i) <= r*c )
    % rear of airfoil
    theta = atan(d_yc_2(x(i)));
    x_u(i) = x(i) - y_t(x(i)) * sin(theta);
    y_u(i) = yc_2(x(i)) + y_t(x(i)) * cos(theta);
    
    x_l(i) = x(i) + y_t(x(i)) * sin(theta);
    y_l(i) = yc_2(x(i)) - y_t(x(i)) * cos(theta);
  elseif ( r*c < x(i) && x(i) <= c )
    % rounded edge.
    theta = atan(d_yc_2(x(i)));
 
    rad = y_t(r*c);
    y_t_blend = @(x) sqrt( (rad)^2 - (x - r*c)^2 );
    
    x_u(i) = x(i) - y_t_blend(x(i)) * sin(theta);
    y_u(i) = yc_2(x(i)) + y_t_blend(x(i)) * cos(theta);
    
    x_l(i) = x(i) + y_t_blend(x(i)) * sin(theta);
    y_l(i) = yc_2(x(i)) - y_t_blend(x(i)) * cos(theta);
 end
end

% take the real part becuase there is a very small imaginary component on
% the trailing edge.
x_l = real(x_l);
y_l = real(y_l);
x_u = real(x_u);
y_u = real(y_u);

% %Verify that points match a the points provided on airfoiltools.com
%points = dlmread('NACA 6512.txt','\t',0,0);
%plot(points(:,1),points(:,2));
%axis equal;
%hold on;

% plot to verify that everything looks okay.
plot(x_u,y_u,'ro',x_l,y_l,'g*')
axis equal;

% put points into the airfoiltools.com format.
A = zeros( numtotalpts , 2 );
A(1:numpoints,1) = x_u;
A(1:numpoints,2) = y_u;

x_l = flipud(x_l);
y_l = flipud(y_l);
A(numpoints+1:numtotalpts,1) = x_l(2:numpoints);
A(numpoints+1:numtotalpts,2) = y_l(2:numpoints);

% write the files to a tab delimited file.
dlmwrite('NACA Airfoil Curve.txt',A,'\t');