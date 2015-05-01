python-lsystems
===============
This is a simple python library created to draw L-systems using python's turtle graphics. Explanation of L-systems can be found here:
http://en.wikipedia.org/wiki/L-system

This library works by reading the details of an L-system specified by a .lsys file. Example L-systems are available in the systems folder. The syntax of the .lsys files is not all-inclusive, but it can be used to run many systems. Within the .lsys file, the variables, constants, and starting configuration must be specified. the vrules section defines the transformation rules for each variable in each iteration, and the crules section defines what effect each constant and variable has, in terms of the turtle graphics. The draw length and other similar variables are contained in the python object used to draw the system.
