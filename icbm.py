#!/usr/bin/python

import sys
import math

G = 6.67408E-11
M = 5.972E+24
R = 6.371E+6

if len(sys.argv) < 3:
    sys.stderr.write("USAGE: python icbm.py Vi Angle\n")
    exit(1)

vi = float(sys.argv[1])*1000.0
angle = float(sys.argv[2])*math.pi/180.0
v  = [ vi*math.cos(angle), vi*math.sin(angle) ]
x  = [ 0.0, R ]
dt = 1.0
r  = rmax = rprev = R
t  = 0.0

# initial acceleration
a = [ -G*M*x[k]/r/r/r for k in range(0,2) ]

# time integration
while True:
    #velocity verlet
    for k in range(0,2):
        v[k] += 0.5*a[k]*dt
        x[k] += v[k]*dt

    rprev = r
    r = math.sqrt(x[0]*x[0]+x[1]*x[1])
    t += dt

    if r < R: break

    for k in range(0,2):
        a[k]  = -G*M*x[k]/r/r/r
        v[k] += 0.5*a[k]*dt

    if r > rmax: rmax = r

# correction of the last position
x = [ x[k]-v[k]*dt for k in range(0,2) ]
t -= dt

dt *= (R-rprev)/(r-rprev)

x = [ x[k]+v[k]*dt for k in range(0,2) ]
t += dt

# maximum altitude
hmax = rmax-R

# maximum distnace
angle = math.acos(x[1]/R)
dist = R*angle

print("max altitude = %.3f km" % (hmax/1000.0))
print("max range    = %.3f km" % (dist/1000.0))

